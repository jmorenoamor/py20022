import random
import string
from datetime import datetime

import dexml
from dexml import fields

def iso_date(date=None):
    ''' Return date in ISO Date Time format '''
    if not date:
        date = datetime.now()
    return date.strftime("%Y-%m-%d")

def iso_datetime(date=None):
    ''' Return date in ISO Date Time format '''
    if not date:
        date = datetime.now()
    return date.strftime("%Y-%m-%dT%H:%M:%S")

def message_id(size=24, chars=string.ascii_uppercase + string.digits):
    ''' Generador de identificador de mensaje '''
    date = datetime.now().strftime("%Y%m%d")
    return date + 'MSG' + ''.join(random.choice(chars) for _ in range(size))

def payment_id(size=24, chars=string.ascii_uppercase + string.digits):
    ''' Generador de identificador de pago '''
    date = datetime.now().strftime("%Y%m%d")
    return date + 'PMT' + ''.join(random.choice(chars) for _ in range(size))

def generated_id(size=35, chars=string.ascii_uppercase + string.digits):
    ''' Generador de identificador '''
    date = datetime.now().strftime("%Y%m%d")
    return date + 'PMT' + ''.join(random.choice(chars) for _ in range(size - 11))

def clean_string(string, size):
    ''' Limpia una cadena de texto según el estandar ISO 20022 '''
    return string[0:size].replace('ñ', 'n').replace('Ñ', 'N').replace('ç', 'c').replace('Ç', 'C')


class Identification(dexml.Model):
    '''Identificación única e inequívoca de la cuenta del acreedor.'''

    iban = fields.String(tagname="IBAN")

    class meta:
        tagname = "Id"

class FinancialInstitutionIdentification(dexml.Model):
    '''Identificación única e inequívoca de una entidad de crédito, asignada en virtud de un esquema internacional reconocido de identificación.'''

    bic = fields.String(tagname="BIC", required=False)

    class meta:
        tagname = "FinInstnId"

class Creditor(dexml.Model):
    '''Información relativa al acreedor.'''

    name = fields.String(tagname="Nm", required=False)

    def __init__(self):
        pass

    def render(self, **kwargs):
        self.name = clean_string(self.name, 70)

        return super(Creditor, self).render(**kwargs)

    class meta:
        tagname = "Cdtr"

class CreditorAccount(dexml.Model):
    '''Identificación inequívoca de la cuenta del acreedor AT-04.'''

    identification = fields.Model(Identification)

    def __init__(self):
        self.identification = Identification()

    class meta:
        tagname = "CdtrAcct"

class CreditorAgent(dexml.Model):
    '''Entidad de crédito donde el acreedor mantiene su cuenta.'''

    financial_institution_identification = fields.Model(FinancialInstitutionIdentification)

    def __init__(self):
        self.financial_institution_identification = FinancialInstitutionIdentification()

    class meta:
        tagname = "CdtrAgt"

class Other(dexml.Model):
    '''Identificación única de una parte, asignada por una institución, mediante un esquema de identificación.'''

    identification = fields.String(tagname="Id")

    def __init__(self):
        pass

    class meta:
        tagname = "Othr"

class PrivateIdentification(dexml.Model):
    '''Identificación única e inequívoca de la parte'''

    other = fields.Model(Other)

    def __init__(self):
        self.other = Other()

    class  meta(object):
        tagname = "PrvtId"

class OrganisationIdentification(dexml.Model):
    '''Identificación única e inequívoca de una persona jurídica.'''

    other = fields.Model(Other, required=False)

    def __init__(self):
        self.other = Other()

    class meta:
        tagname = "OrgId"

class Identification_Private(dexml.Model):
    '''Identificación única e inequívoca de la parte'''

    private_identification = fields.Model(PrivateIdentification)

    def __init__(self):
        self.private_identification = PrivateIdentification()

    class  meta(object):
        tagname = "Id"

class Identification_Organisation(dexml.Model):
    '''Identificación única e inequívoca de la parte'''

    organisation_identification = fields.Model(OrganisationIdentification)

    def __init__(self):
        self.organisation_identification = OrganisationIdentification()

    class  meta(object):
        tagname = "Id"

class CreditorSchemeIdentification(dexml.Model):
    '''Identificación del acreedor'''

    identification = fields.Model(Identification_Private)

    def __init__(self):
        self.identification = Identification_Private()

    class  meta(object):
        tagname = "CdtrSchmeId"

class PaymentIdentification(dexml.Model):
    '''Conjunto de elementos que sirven de referencia de una instrucción de pago.'''

    instruction_identification = fields.String(tagname="InstrId", required=False)
    end_to_end_identification = fields.String(tagname='EndToEndId')

    def __init__(self):
        self.end_to_end_identification = generated_id(35)

    def render(self, **kwargs):
        self.end_to_end_identification = clean_string(self.end_to_end_identification, 35)

        return super(PaymentIdentification, self).render(**kwargs)

    class meta:
        tagname = "PmtId"

class InstructedAmount(dexml.Model):
    '''Importe del adeudo directo expresado en euros (AT-06).'''

    currency = fields.String(attrname="Ccy")
    amount = fields.String(tagname=".")

    def __init__(self):
        self.currency = "EUR"

    class meta:
        tagname = "InstdAmt"

class RemittanceInformation(dexml.Model):
    '''Información que opcionalmente remite el acreedor al deudor para permitirle conciliar el pago con la información comercial del mismo (AT-22).'''

    unstructured = fields.String(tagname="Ustrd")

    def __init__(self):
        self.unstructured = ""

    def render(self, **kwargs):
        self.unstructured = clean_string(self.unstructured, 140)

        return super(RemittanceInformation, self).render(**kwargs)

    class meta:
        tagname = "RmtInf"

class DebtorAgent(dexml.Model):
    '''Entidad de crédito donde el deudor mantiene su cuenta (AT-13).'''

    financial_institution_identification = fields.Model(FinancialInstitutionIdentification)

    def __init__(self):
        self.financial_institution_identification = FinancialInstitutionIdentification()

    class meta:
        tagname = "DbtrAgt"

class Debtor(dexml.Model):
    '''Información relativa al deudor.'''

    name = fields.String(tagname="Nm", required=False)

    def __init__(self):
        pass

    def render(self, **kwargs):
        self.name = clean_string(self.name, 70)

        return super(Creditor, self).render(**kwargs)

    class meta:
        tagname = "Dbtr"

class DebtorAccount(dexml.Model):
    '''Identificación inequívoca de la cuenta del deudor donde se cargará el adeudo directo (AT-07).'''

    identification = fields.Model(Identification)

    def __init__(self):
        self.identification = Identification()

    class meta:
        tagname = "DbtrAcct"

class MandateRelatedInformation(dexml.Model):
    '''Conjunto de elementos utilizado para suministrar mayor información sobre el mandato firmado entre acreedor y deudor.'''
    """Este elemento es de uso obligatorio. Si la etiqueta 2.50 ‘Indicador de modificación’ tiene el valor ‘false’,
    no se permite la presencia del elemento 2.51 ‘Detalles de la modificación’. Si la etiqueta 2.50 ‘Indicador de modificación’
    tiene el valor ‘true’, el elemento 2.51 ‘Detalles de la modificación’ debe estar presente.
    """
    mandate_identification = fields.String(tagname="MndtId")
    date_of_signature = fields.String(tagname="DtOfSgntr")

    def __init__(self):
        self.mandate_identification = generated_id(35)
        self.date_of_signature = iso_date()

    class meta:
        tagname = "MndtRltdInf"

class DirectDebitTransaction(dexml.Model):
    '''Conjunto de elementos que suministran información específica relativa al mandato de adeudo directo.'''

    mandate_related_information = fields.Model(MandateRelatedInformation)

    def __init__(self):
        self.mandate_related_information = MandateRelatedInformation()

    class meta:
        tagname = "DrctDbtTx"

class DirectDebitTransactionInformation(dexml.Model):
    '''Conjunto de elementos utilizados para proporcionar información sobre cada una de las operaciones individuales incluidas en el mensaje.'''

    payment_identification = fields.Model(PaymentIdentification)
    instructed_amount = fields.Model(InstructedAmount)
    charge_bearer = fields.String(tagname="ChrgBr")
    direct_debit_transaction = fields.Model(DirectDebitTransaction)
    debtor_agent = fields.Model(DebtorAgent)
    debtor = fields.Model(Debtor)
    debtor_account = fields.Model(DebtorAccount)
    remittance_information = fields.Model(RemittanceInformation)

    def __init__(self):
        self.payment_identification = PaymentIdentification()
        self.instructed_amount = InstructedAmount()
        self.charge_bearer = "SLEV"
        self.debtor_agent = DebtorAgent()
        self.debtor = Debtor()
        self.debtor_account = DebtorAccount()
        self.direct_debit_transaction = DirectDebitTransaction()

    class meta:
        tagname = "DrctDbtTxInf"

class LocalInstrument(dexml.Model):
    '''Instrumento específico del esquema SEPA.'''

    code = fields.String(tagname="Cd")

    def __init__(self):
        self.code = "CORE"

    class meta:
        tagname = "LclInstrm"

class ServiceLevel(dexml.Model):
    '''Acuerdo o reglas que rigen cómo debe procesarse la operación.'''

    code = fields.String(tagname="Cd")

    def __init__(self):
        self.code = "SEPA"

    class meta:
        tagname = "SvcLvl"

class PaymentTypeInformation(dexml.Model):
    '''Conjunto de elementos utilizados para especificar con mayor detalle el tipo de operación.'''

    service_level = fields.Model(ServiceLevel)
    local_instrument = fields.Model(LocalInstrument)
    sequence_type = fields.String(tagname="SeqTp")

    def __init__(self):
        self.service_level = ServiceLevel()
        self.local_instrument = LocalInstrument()
        self.sequence_type = "OOFF"

    class meta:
        tagname = "PmtTpInf"

class PaymentInformation(dexml.Model):
    payment_information_identification = fields.String(tagname="PmtInfId")
    payment_method = fields.String(tagname="PmtMtd")
    payment_type_information =  fields.Model(PaymentTypeInformation)
    requested_collection_date = fields.String(tagname="ReqdColltnDt")
    creditor = fields.Model(Creditor)
    creditor_account = fields.Model(CreditorAccount)
    creditor_agent = fields.Model(CreditorAgent)
    creditor_scheme_identification = fields.Model(CreditorSchemeIdentification)
    direct_debit_transaction_information = fields.Model(DirectDebitTransactionInformation)

    def __init__(self, payment_id=None):
        self.payment_type_information = PaymentTypeInformation()
        if not payment_id:
            self.payment_information_identification = generated_id(35)
        self.requested_collection_date = iso_date()
        self.creditor = Creditor()
        self.creditor_account = CreditorAccount()
        self.creditor_agent = CreditorAgent()
        self.direct_debit_transaction_information = DirectDebitTransactionInformation()
        self.creditor_scheme_identification = CreditorSchemeIdentification()
        self.payment_method = "DD"

    def render(self, **kwargs):
        self.payment_information_identification = clean_string(self.payment_information_identification, 35)
        self.requested_collection_date = clean_string(self.requested_collection_date, 2)

        return super(PaymentInformation, self).render(**kwargs)

    class meta:
        tagname = "PmtInf"

class InitiatingParty(dexml.Model):
    '''Parte que presenta el mensaje. En el mensaje de presentación, puede ser el “acreedor” o “el presentador”.'''

    name = fields.String(tagname="Nm", required=False)
    # identification = fields.String(tagname="Id", required=False)
    identification = fields.Model(Identification_Organisation)

    def __init__(self):
        self.identification = Identification_Organisation()

    class meta:
        tagname = "InitgPty"

class GroupHeader(dexml.Model):
    '''Conjunto de características compartidas por todas las operaciones incluidas en el mensaje.'''

    message_identification = fields.String(tagname='MsgId')
    creation_date_time = fields.String(tagname='CreDtTm')
    number_of_transactions = fields.String(tagname='NbOfTxs')
    control_sum = fields.Float(tagname="CtrlSum", required=False)
    initiating_party = fields.Model(InitiatingParty)

    def __init__(self):
        self.message_identification = generated_id(35)
        self.creation_date_time = iso_datetime()
        self.initiating_party = InitiatingParty()
        self.number_of_transactions = "1"

    def render(self, **kwargs):
        return super(GroupHeader, self).render(**kwargs)

    class meta:
        tagname = "GrpHdr"

class CstmrDrctDbtInitn(dexml.Model):
    '''Identifica el tipo de mensaje: iniciación de adeudos directos.'''

    header = fields.Model(GroupHeader)
    # payment_information = fields.Model(PaymentInformation)
    payment_information = fields.List(PaymentInformation)

    def __init__(self):
        self.header = GroupHeader()
        # self.payment_information = PaymentInformation()
        self.payment_information = list()

    class meta:
        tagname = "CstmrDrctDbtInitn"

class Document(dexml.Model):
    '''Clase base.'''

    namespaces = """<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02" xmlns:asx="http://www.sap.com/abapxml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">"""

    operation = fields.Model(CstmrDrctDbtInitn)

    def __init__(self):
        self.operation = CstmrDrctDbtInitn()

    def render(self, **kwargs):
        return super(Document, self).render(**kwargs).replace('<Document>', self.namespaces)

    class meta:
        tagname = "Document"
        # namespace = "urn:iso:std:iso:20022:tech:xsd:pain.008.001.02"
