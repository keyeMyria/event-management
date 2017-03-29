from datetime import datetime

from app.helpers.cache import cache
from app.helpers.data import save_to_db
from app.helpers.helpers import get_count, represents_int
from app.helpers.payment import StripePaymentsManager, PayPalPaymentsManager
from app.models.discount_code import DiscountCode, EVENT
from app.models.event import Event
from app.models.event_invoice import EventInvoice


class InvoicingManager(object):
    """All event service fee invoicing related functions"""

    @cache.memoize(50)
    def get_invoice(self, invoice_id):
        return EventInvoice.query.get(invoice_id)

    @staticmethod
    def get_invoice_by_identifier(identifier):
        return EventInvoice.query.filter_by(identifier=identifier).first()

    @staticmethod
    def get_discount_codes():
        return DiscountCode.query.filter_by(used_for=EVENT).all()

    @staticmethod
    def get_discount_code_used_count(discount_code_id):
        return get_count(Event.query.filter_by(discount_code_id=discount_code_id))

    @staticmethod
    def get_discount_code(discount_code):
        if represents_int(discount_code):
            return DiscountCode.query.filter_by(id=discount_code).filter_by(used_for=EVENT).first()
        else:
            return DiscountCode.query.filter_by(code=discount_code).filter_by(used_for=EVENT).first()

    @staticmethod
    def get_invoices(event_id=None, status=None, from_date=None, to_date=None):
        if event_id:
            if status:
                invoices = EventInvoice.query.filter_by(event_id=event_id).filter_by(status=status)
            else:
                invoices = EventInvoice.query.filter_by(event_id=event_id)
        else:
            if status:
                invoices = EventInvoice.query.filter_by(status=status)
            else:
                invoices = EventInvoice.query

        if from_date:
            invoices = invoices.filter(EventInvoice.created_at >= from_date)
        if to_date:
            invoices = invoices.filter(EventInvoice.created_at <= to_date)
        return invoices.all()

    @staticmethod
    def get_invoices_count(event_id, status='completed'):
        return get_count(EventInvoice.query.filter_by(event_id=event_id).filter_by(status=status))

    @staticmethod
    def initiate_invoice_payment(form):
        identifier = form['identifier']
        email = form['email']

        invoice = InvoicingManager.get_invoice_by_identifier(identifier)
        if invoice:
            user = invoice.user
            if invoice.amount > 0 \
                and (not invoice.paid_via
                     or (invoice.paid_via
                         and (invoice.paid_via == 'stripe'
                              or invoice.paid_via == 'paypal'))):

                country = form['country']
                address = form['address']
                city = form['city']
                state = form['state']
                zipcode = form['zipcode']
                invoice.address = address
                invoice.city = city
                invoice.state = state
                invoice.country = country
                invoice.zipcode = zipcode
                invoice.status = 'initialized'
            else:
                invoice.status = 'completed'
                invoice.completed_at = datetime.utcnow()
                if not invoice.paid_via:
                    invoice.paid_via = 'free'
            save_to_db(invoice)
            return invoice
        else:
            return False

    @staticmethod
    def charge_stripe_invoice_payment(form):
        invoice = InvoicingManager.get_invoice_by_identifier(form['identifier'])
        invoice.stripe_token = form['stripe_token_id']
        save_to_db(invoice)

        charge = StripePaymentsManager.capture_payment(invoice, credentials=StripePaymentsManager.get_credentials())
        if charge:
            invoice.paid_via = 'stripe'
            invoice.payment_mode = charge.source.object
            invoice.brand = charge.source.brand
            invoice.exp_month = charge.source.exp_month
            invoice.exp_year = charge.source.exp_year
            invoice.last4 = charge.source.last4
            invoice.transaction_id = charge.id
            invoice.status = 'completed'
            invoice.completed_at = datetime.utcnow()
            save_to_db(invoice)

            return True, invoice
        else:
            return False, 'Error'

    @staticmethod
    def charge_paypal_invoice_payment(invoice):
        payment_details = PayPalPaymentsManager \
            .get_approved_payment_details(invoice, credentials=PayPalPaymentsManager.get_credentials())

        if 'PAYERID' in payment_details:
            capture_result = PayPalPaymentsManager \
                .capture_payment(invoice, payment_details['PAYERID'],
                                 credentials=PayPalPaymentsManager.get_credentials())

            if capture_result['ACK'] == 'Success':
                invoice.paid_via = 'paypal'
                invoice.status = 'completed'
                invoice.transaction_id = capture_result['PAYMENTINFO_0_TRANSACTIONID']
                invoice.completed_at = datetime.utcnow()
                save_to_db(invoice)
                return True, invoice
            else:
                return False, capture_result['L_SHORTMESSAGE0']
        else:
            return False, 'Payer ID missing. Payment flow tampered.'

    @staticmethod
    def create_edit_discount_code(form, discount_code_id=None):
        if not discount_code_id:
            discount_code = DiscountCode()
        else:
            discount_code = InvoicingManager.get_discount_code(discount_code_id)
        discount_code.code = form.get('code')
        discount_code.value = form.get('value')
        discount_code.type = 'percent'
        discount_code.max_quantity = form.get('max_quantity', None)
        discount_code.tickets_number = form.get('tickets_number')
        discount_code.used_for = EVENT
        discount_code.marketer_id = form.get('marketer')
        discount_code.is_active = form.get('status', 'in_active') == 'active'

        if discount_code.max_quantity == "":
            discount_code.max_quantity = None

        try:
            discount_code.valid_from = datetime.strptime(form.get('start_date', None) + ' ' +
                                                         form.get('start_time', None), '%m/%d/%Y %H:%M')
        except:
            discount_code.valid_from = None

        try:
            discount_code.valid_till = datetime.strptime(form.get('end_date', None) + ' ' +
                                                         form.get('end_time', None), '%m/%d/%Y %H:%M')
        except:
            discount_code.valid_till = None

        save_to_db(discount_code)

        return discount_code
