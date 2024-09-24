YES_NO_OPTIONS = (
    ('Y', 'YES'),
    ('N', 'NO'),
)

CLASSIFICATION = (
    (1, 'Haberes'),
    (2, 'Descuentos'),
)

TYPE_CLASSIFICATION = (
    (1, 'Imponible'),
    (2, 'No Imponible'),
    (3, 'Previsional'),
    (4, 'Judicial'),
    (5, 'Tributario'),
    (6, 'Acordado')
)

SEARCH_FIELDS = (
    ('0', ' --------- '),
    ('ISAPRE', 'isapre'),
    ('FONASA', 'fonasa'),
    ('AFP', 'afp'),
)

REMUNERATION_TYPE = (
    (0, ' --------- '),
    (1, 'Sueldo'),
    (2, 'Sobresueldo'),
    (3, 'Variable'),
    (4, 'Eventuales'),
    (5, 'Gratificación'),
    (6, 'Descuento')
)

TITLES = (
    (0, ' --------- '),
    (1, 'RENTAS TOPES IMPONIBLES'),
    (2, 'RENTAS MÍNIMAS IMPONIBLES'),
    (3, 'AHORRO PREVISIONAL VOLUNTARIO (APV)'),
    (4, 'DEPÓSITO CONVENIDO'),
)

TYPE_VARIABLE = (
    (0, ' --------- '),
    (1, 'PREVIRED'),
    (2, 'REMUNERACIONES'),
)

SEX_OPTIONS = (
    ('M', 'MASCULINO'),
    ('F', 'FEMENINO'),
)

CIVIL_STATUS_OPTIONS = (
    (1, 'Solter@'),
    (2, 'Casad@'),
    (3, 'Divorciad@'),
    (4, 'Viud@'),
)

USER_TYPE_OPTIONS = (
    (1, 'Super-Admin'),
    (2, 'Recursos Humanos'),
    (3, 'Recursos Humanos Administrador'),
    (4, 'Jefatura'),
    (5, 'Colaborador'),
)

PAYMENT_METHOD_OPTIONS = (
    (1, 'Efectivo'),
    (2, 'Cheque'),
    (3, 'Vale vista'),
    (4, 'Depósito directo'),
)

BANK_ACCOUNT_TYPE_OPTIONS = (
    (1, 'Cuenta Vista'),
    (2, 'Cuenta de Ahorro'),
    (3, 'Cuenta Bancaria para Estudiante'),
    (4, 'Cuenta Chequera Electrónica'),
    (5, 'Cuenta Rut'),
    (6, 'Cuenta Bancaria para Extranjeros'),
    (7, 'Cuenta Corriente'),
)

STUDY_TYPE_OPTIONS = (
    (1, 'Enseñanza Media'),
    (2, 'Estudios Superiores (CFT)'),
    (3, 'Estudios Universitarios'),
)

STUDY_STATUS_OPTIONS = (
    (1, 'Completo'),
    (2, 'Incompleto'),
)

WORKER_TYPE = (
    (0, '[seleccione]'),
    (1, 'Activo (no pensionado)'),
    (2, 'Pensionado y cotiza AFP'),
    (3, 'Pensionado y no cotiza AFP'),
    (4, 'Activo mayor de 65 años (nunca pensionado)'),
)

OPCIONES = (
    ('S', 'SI'),
    ('N', 'NO'),
)

NOTIFICATION = (
    ('E', 'Email'),
    ('C', 'Carta'),
)

AMOUNT_TYPE = (
    ('P', 'Porcentaje'),
    ('M', 'Monto'),
)

TYPE_GRATIFICATION = (
    ('A', 'Anual'),
    ('M', 'Mensual'),
)

CONTRACT_TYPE = (
    ('', '[seleccione]'),
    ('PI', 'Plazo Indefinido'),
    ('PF', 'Plazo Fijo'),
    ('PI11', 'Plazo Indefinido 11 años o más'),
    ('TCP', 'Trabajador de Casa Particular'),
)

FAMILY_ALLOWANCE_SECTION = (
    (0, '---------'),
    (1, 'A'),
    (2, 'B'),
    (3, 'C'),
    (4, 'D'),
)

ESTATE_JOB = (
    (0, '[seleccione]'),
    (1, 'Vigente'),
    (2, 'Desvinculado')
)

CONTRIBUTION_TYPE = (
    (0, '---------'),
    (1, 'PESOS ($)'),
    (2, 'PORCENTAJE (%)'),
    (3, 'UNIDAD DE FOMENTO (UF)'),
)

TAX_REGIME = (
    (0, '---------'),
    (1, 'APV Regimen A'),
    (2, 'APV Regimen B'),
    (3, 'Depósitos Convenidos(**)'),
)

SHAPE = (
    (0, '---------'),
    (1, 'DIRECTA'),
    (2, 'INDIRECTA'),
)

WORKER_SECTOR = (
    (0, '[seleccione]'),
    (1, 'Público'),
    (2, 'Privado'),
)

ALL_DAYS = (
    ('Lunes', 'Lunes'),
    ('Martes', 'Martes'),
    ('Miércoles', 'Miércoles'),
    ('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),
    ('Sábado', 'Sábado'),
    ('Domingo', 'Domingo'),
)

HEALTH_ENTITY_TYPE = (
    ('F', 'FONASA'),
    ('I', 'ISAPRE'),
)

TYPE_USERS = (
    (1, 'Admin'),
    (2, 'HR Manager'),
    (3, 'Colaborador'),
    (4, 'Supervisor'),
)