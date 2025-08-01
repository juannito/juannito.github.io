from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from spider.views import twilio_webhooks  # twilio
from spider.views import inversiones_en_propiedades
from spider.views.agrupador import AgrupadorViewSet
from spider.views.alquiler import AlquilerViewSet
from spider.views.archivo import ArchivoViewSet
from spider.views.casos import CasoViewSet
from spider.views.clients_notifications import ClientNotificationViewSet
from spider.views.clients_notifications_templates import \
    ClientNotificationTemplateViewSet
from spider.views.comentarios_caso import ComentarioCasoViewSet
from spider.views.comentarios_orden import ComentarioOrdenViewSet
from spider.views.comentarios_solicitud_retiro import \
    ComentarioSolicitudRetiroViewSet
from spider.views.comentarios_transaccion import ComentarioTransaccionViewSet
from spider.views.comprobantes_bitpay import ComprobanteBitpayViewSet
from spider.views.configuracion import ConfiguracionViewSet
from spider.views.contactos import ContactoViewSet
from spider.views.contratistas import ContratistaViewSet
from spider.views.contratistas_orden import ContratistaOrdenViewSet
from spider.views.cuenta_bancaria import CuentaBancariaViewSet
from spider.views.cuotas_caso_resolution import CuotaCasoResolutionViewSet
from spider.views.detalle_solicitudes_retiro import \
    DetalleSolicitudRetiroViewSet
from spider.views.documento_de_propiedad import DocumentoDePropiedadViewSet
from spider.views.documentodesociedad import DocumentoDeSociedadViewSet
from spider.views.documentos_de_hipoteca import DocumentoDeHipotecaViewSet
from spider.views.documentos_de_propiedad_de_hipoteca import \
    DocumentoDePropiedadDeHipotecaViewSet
from spider.views.etiquetas_de_hipoteca import EtiquetaDeHipotecaViewSet
from spider.views.etiquetas_perfil import EtiquetaPerfilViewSet
from spider.views.etiquetas_por_perfil import EtiquetaPorPerfilViewSet
from spider.views.fractionals import FractionalViewSet
from spider.views.hipotecas import HipotecaViewSet
from spider.views.home import home
from spider.views.imagenes_pdf import ImagenPDFViewSet
from spider.views.inquilinos import InquilinoViewSet
from spider.views.inversion import InversionViewSet
from spider.views.inversiones_en_propiedades import InversionEnPropiedadViewSet
from spider.views.firma_inversion import FirmaInversionViewSet 
from spider.views.settings import SettingsViewSet
from spider.views.inversiones_hipoteca import InversionHipotecaViewSet
from spider.views.invitacion import InvitacionViewSet
from spider.views.job import JobViewSet
from spider.views.mensajes_inbox import MensajeInboxViewSet
from spider.views.metamap import MetamapViewSet
from spider.views.my_custom_auth import CustomAuthToken
from spider.views.my_custom_oauth import CustomOAuthToken
from spider.views.mis_propiedades import MisPropiedadesViewSet
from spider.views.no_auth_view import NoAuthViewSet
from spider.views.notificacion import NotificacionViewSet
# from spider.views.plantillas_whatsapp import PlantillaWhatsappViewSet
# from spider.views.parametros_plantilla_whatsapp import ParametroPlantillaWhatsappViewSet
from spider.views.notificaciones_webinar import NotificacionWebinarViewSet
from spider.views.ordenes_mantenimiento import OrdenMantenimientoViewSet
from spider.views.organizacion import OrganizacionViewSet
from spider.views.overdue_court_days import OverdueCourtDayViewSet
from spider.views.paginas_estaticas import pagina_estatica_view
from spider.views.pagos import PagoViewSet as SpiderPagoViewSet
from spider.views.pais import PaisViewSet
from spider.views.participacion import ParticipacionViewSet
from spider.views.perfil import PerfilViewSet
from spider.views.perfiles_de_inversores import PerfilDeInversorViewSet
from spider.views.plantilla_notificacion import PlantillaNotificacionViewSet
from spider.views.property_managers import PropertyManangerViewSet
from spider.views.propiedad import PropiedadViewSet, PropertySimplifiedViewSet
from spider.views.propiedades_de_hipoteca import PropiedadDeHipotecaViewSet
from spider.views.propuesta_de_propiedad_alquileres import \
    PropuestaDePropiedadAlquilerViewSet
from spider.views.propuesta_de_propiedad_empresas import \
    PropuestaDePropiedadEmpresaViewSet
from spider.views.propuesta_de_propiedad_fotos import \
    PropuestaDePropiedadFotoViewSet
from spider.views.propuesta_de_propiedad_inquilinos import \
    PropuestaDePropiedadInquilinoViewSet
from spider.views.propuesta_de_propiedad_logs import \
    PropuestaDePropiedadLogViewSet
from spider.views.propuesta_de_propiedad_personales import \
    PropuestaDePropiedadPersonalViewSet
from spider.views.propuesta_de_propiedad_tipos_de_propiedad import \
    PropuestaDePropiedadTipoDePropiedadViewSet
from spider.views.propuesta_de_propiedad_unidades import \
    PropuestaDePropiedadUnidadViewSet
from spider.views.propuestas_de_propiedad import PropuestaDePropiedadViewSet
from spider.views.proyecto import ProyectoViewSet
from spider.views.recurso import RecursoArchivoViewSet, RecursoViewSet
from spider.views.roles import RolViewSet
from spider.views.sociedad import SociedadViewSet
from spider.views.entity_pot import EntityPotViewSet
from spider.views.solicitudes_retiro import SolicitudRetiroViewSet
from spider.views.states import StateViewSet
from spider.views.stripe_payment_intents import StripePaymentIntentViewSet
from spider.views.subtipo import SubtipoViewSet
from spider.views.tag import TagViewSet
from spider.views.tags_mensaje_inbox import TagMensajeInboxViewSet
from spider.views.tags_recordatorio_mensaje_inbox import \
    TagRecordatorioMensajeInboxViewSet
from spider.views.tareas import TareaViewSet
from spider.views.tareas_mantenimiento import TareaMantenimientoViewSet
from spider.views.tareas_mantenimiento_multimedia import \
    TareaMantenimientoMultimediaViewSet
from spider.views.tipo import TipoViewSet
from spider.views.tipodedocumento import TipoDeDocumentoViewSet
from spider.views.tipos_de_documento_para_sociedad import \
    TipoDeDocumentoParaSociedadViewSet
from spider.views.tipos_de_hipoteca import TipoDeHipotecaViewSet
from spider.views.tipos_mantenimiento import TipoMantenimientoViewSet
from spider.views.transaccion import TransaccionViewSet
from spider.views.transacciones_de_inversion import \
    TransaccionDeInversionViewSet
from spider.views.transacciones_vinculada import TransaccionVinculadaViewSet
from spider.views.ultimo_acceso_usuario import UltimoAccesoUsuarioViewSet
from spider.views.urls_webinar import UrlWebinarViewSet
from spider.views.zoom_webinars import ZoomWebinarViewSet

from spider.views.insurance_policies import InsurancePolicyViewSet
from spider.views.insurance_companies import InsuranceCompanyViewSet
from spider.views.plaid_identity_verifications import PlaidIdentityVerificationViewSet
from spider.views.property_manager_agreements import PropertyManagerAgreementViewSet
from spider.views.transactions_mv import TransactionMVViewSet
from spider.views.plaid_transactions import PlaidTransactionViewSet
from spider.views.plaid_bank_accounts import PlaidBankAccountViewSet
from spider.views.plaid_bank_transactions import PlaidBankTransactionViewSet
from spider.views.plaid_bank_subaccounts import PlaidBankSubaccountViewSet
from spider.views.geocode import GeocodeViewSet
from spider.views.service import ServiceViewSet, ServiceCategoryViewSet
from spider.views.service_bundle import ServiceBundleViewSet
from spider.views.transaccion_de_servicio import TransaccionDeServicioViewSet
from spider.views.transfers import TransferirBalanceView

from spider.views.admin_groups_permissions import GroupViewSet, PermissionViewSet

# Mercury API endpoints
from spider.views.mercury import (
    society_snapshot, submit_onboarding_data, 
    mercury_webhook, mercury_status
)



# IQUALITY
# from iq.views.proyectos import ProyectoViewSet as ProyectoIQViewSet
# from iq.views.socios_estrategicos import SocioEstrategicoViewSet
# from iq.views.pagina import PaginaViewSet
# from iq.views.perfiles import PerfilViewSet as PerfilIQViewSet
# from iq.views.cuenta_bancaria import CuentaBancariaViewSet as CuentaBancariaIQViewSet
# from iq.views.notificaciones import NotificacionViewSet as NotificacionIQViewSet
# from iq.views.invitaciones import InvitacionViewSet as InvitacionIQViewSet
# from iq.views.activos import ActivoViewSet
# from iq.views.detalles_oportunidad import DetalleOportunidadViewSet
# from iq.views.inversiones_individuales import InversionIndividualViewSet
# from iq.views.acontecimientos_proyecto import AcontecimientoProyectoViewSet
# from iq.views.contratos import subscription_agreements, offering_memorandum
# from iq.views.pagos import PagoViewSet

router = routers.DefaultRouter(trailing_slash=False)

# Rutas de spider
router.register("tipo-de-documento-para-sociedades", TipoDeDocumentoParaSociedadViewSet)
router.register("transacciones", TransaccionViewSet)
router.register("perfiles", PerfilViewSet, basename="perfiles")
router.register("sociedades", SociedadViewSet)
router.register("entity-pot", EntityPotViewSet, basename="entity_pot")
router.register("participaciones", ParticipacionViewSet)
router.register("paises", PaisViewSet, basename="paises")
router.register("propiedades", PropiedadViewSet, basename="propiedad")
router.register("proyectos", ProyectoViewSet)
router.register("tipos", TipoViewSet)
router.register("subtipos", SubtipoViewSet)
router.register("archivos", ArchivoViewSet)
router.register("tags", TagViewSet)
router.register("tipos-de-documentos", TipoDeDocumentoViewSet)
router.register("documentos-de-sociedad", DocumentoDeSociedadViewSet)
router.register("recursos", RecursoViewSet)
router.register("recursos-archivo", RecursoArchivoViewSet)
router.register("inversiones", InversionViewSet)
router.register("organizaciones", OrganizacionViewSet)
router.register("alquileres", AlquilerViewSet)
router.register("imagenes-pdf", ImagenPDFViewSet)  # hay que revisar el frontend
router.register("documentos-de-propiedad", DocumentoDePropiedadViewSet)
router.register("invitaciones", InvitacionViewSet)
router.register("path", NoAuthViewSet, basename="path")
router.register("cuentas-bancarias", CuentaBancariaViewSet)
router.register("plantillas-notificacion", PlantillaNotificacionViewSet)
router.register("notificaciones", NotificacionViewSet)
router.register("ultimo-acceso-usuarios", UltimoAccesoUsuarioViewSet)
router.register("agrupadores", AgrupadorViewSet)
router.register("property-managers", PropertyManangerViewSet)
router.register("contactos", ContactoViewSet)
router.register("inquilinos", InquilinoViewSet)
router.register("casos", CasoViewSet)
router.register("comentario-casos", ComentarioCasoViewSet)
router.register("cuotas-caso-resolution", CuotaCasoResolutionViewSet)
router.register("roles", RolViewSet)
router.register("solicitudes-retiro", SolicitudRetiroViewSet)
router.register("detalle-solicitudes-retiro", DetalleSolicitudRetiroViewSet)
router.register("comentario-solicitudes-retiro", ComentarioSolicitudRetiroViewSet)
router.register("comentarios-transaccion", ComentarioTransaccionViewSet)
router.register("pagos", SpiderPagoViewSet)
router.register("zoom-webinars", ZoomWebinarViewSet)
router.register("urls-webinar", UrlWebinarViewSet)
router.register("notificaciones-webinar", NotificacionWebinarViewSet)
router.register("comprobantes-bitpay", ComprobanteBitpayViewSet)
router.register("states", StateViewSet)
router.register("overdue-court-days", OverdueCourtDayViewSet)
router.register("my-properties", MisPropiedadesViewSet, basename="my_properties")

# Mantenimiento
router.register("tareas", TareaViewSet)
router.register("contratistas", ContratistaViewSet)
router.register("contratistas-orden", ContratistaOrdenViewSet)
router.register("tareas-mantenimiento", TareaMantenimientoViewSet)
router.register("ordenes-mantenimiento", OrdenMantenimientoViewSet)
router.register("tipos-mantenimiento", TipoMantenimientoViewSet)
router.register("comentarios-orden", ComentarioOrdenViewSet)
router.register("tareas-mantenimiento-multimedia", TareaMantenimientoMultimediaViewSet)
router.register("job", JobViewSet)
router.register("etiquetas-perfil", EtiquetaPerfilViewSet)
router.register("etiquetas-por-perfil", EtiquetaPorPerfilViewSet)
router.register("mensajes-inbox", MensajeInboxViewSet)
router.register("tags-mensaje-inbox", TagMensajeInboxViewSet)
router.register("tags-recordatorio-mensaje-inbox", TagRecordatorioMensajeInboxViewSet)

# Hipotecas
router.register("documentos-de-hipoteca", DocumentoDeHipotecaViewSet)
router.register("hipotecas", HipotecaViewSet)
router.register("etiquetas_de_hipoteca", EtiquetaDeHipotecaViewSet)
router.register("tipo-de-hipoteca", TipoDeHipotecaViewSet)
router.register("propiedades-de-hipoteca", PropiedadDeHipotecaViewSet)
router.register(
    "documentos-de-propiedad-de-hipoteca", DocumentoDePropiedadDeHipotecaViewSet
)
router.register("inversiones-hipoteca", InversionHipotecaViewSet)
router.register("transacciones-de-inversion", TransaccionDeInversionViewSet)
router.register("transacciones-vinculadas", TransaccionVinculadaViewSet)

# Inversiones
router.register("perfiles-de-inversores", PerfilDeInversorViewSet)
router.register("inversiones-en-propiedades", InversionEnPropiedadViewSet)
router.register("fractionals", FractionalViewSet, basename="fractional")

# Stripe
router.register(
    "stripe/payments-intents",
    StripePaymentIntentViewSet,
    basename="stripe_payments_intents",
)
router.register("metamap", MetamapViewSet, basename="metamap")
# Plaid
router.register("identity-verification", PlaidIdentityVerificationViewSet, basename="identity-verification")
router.register("plaid/transactions", PlaidTransactionViewSet, basename="plaid-transactions")
router.register("plaid/bank-accounts", PlaidBankAccountViewSet)
router.register("plaid/bank-transactions", PlaidBankTransactionViewSet)
router.register("plaid/bank-subaccounts", PlaidBankSubaccountViewSet)

# Configuración
router.register("configuracion", ConfiguracionViewSet, basename="configuracion")
router.register("propuestas-de-propiedad", PropuestaDePropiedadViewSet)
router.register("propuesta-de-propiedad-fotos", PropuestaDePropiedadFotoViewSet)
router.register(
    "propuesta-de-propiedad-tipos-de-propiedad",
    PropuestaDePropiedadTipoDePropiedadViewSet,
)
router.register(
    "propuesta-de-propiedad-personales", PropuestaDePropiedadPersonalViewSet
)
router.register("propuesta-de-propiedad-empresas", PropuestaDePropiedadEmpresaViewSet)
router.register(
    "propuesta-de-propiedad-alquileres", PropuestaDePropiedadAlquilerViewSet
)
router.register(
    "propuesta-de-propiedad-inquilinos", PropuestaDePropiedadInquilinoViewSet
)
router.register("propuesta-de-propiedad-unidades", PropuestaDePropiedadUnidadViewSet)
router.register("propuesta-de-propiedad-logs", PropuestaDePropiedadLogViewSet)
router.register("clients-notifications", ClientNotificationViewSet)
router.register("clients-notifications-templates", ClientNotificationTemplateViewSet)
router.register("insurance-policies", InsurancePolicyViewSet)
router.register("insurance-companies", InsuranceCompanyViewSet)
router.register("property-manager-agreements", PropertyManagerAgreementViewSet)
# django-api-helper router placeholder

router.register("simplified/properties", PropertySimplifiedViewSet, basename="property_simplified")
router.register("transactions", TransactionMVViewSet)

# Rutas firma inversion
router.register("firma-inversion", FirmaInversionViewSet)

# Rutas firma inversion
router.register("settings", SettingsViewSet, basename='settings')

router.register(r'place', GeocodeViewSet, basename='place')

# Rutas de IQ
# router.register("iq/acontecimientos-proyecto", AcontecimientoProyectoViewSet)
# router.register("iq/activos", ActivoViewSet)
# router.register("iq/proyectos", ProyectoIQViewSet)
# router.register("iq/socios-estrategicos", SocioEstrategicoViewSet)
# router.register("iq/paises", PaisViewSet, basename="paises")
# router.register("iq/paginas", PaginaViewSet)
# router.register("iq/organizaciones", OrganizacionViewSet)
# router.register("iq/perfiles", PerfilIQViewSet)
# router.register("iq/cuentas-bancarias", CuentaBancariaIQViewSet)
# router.register("iq/notificaciones", NotificacionIQViewSet)
# router.register("iq/invitaciones", InvitacionIQViewSet)
# router.register("iq/detalles-oportunidad", DetalleOportunidadViewSet)
# router.register("iq/inversiones-individuales", InversionIndividualViewSet)
# router.register("iq/pagos", PagoViewSet)

# Service related routes
router.register("services", ServiceViewSet)
router.register("service-categories", ServiceCategoryViewSet)
router.register("service-bundles", ServiceBundleViewSet)
router.register("transacciones-de-servicio", TransaccionDeServicioViewSet)
router.register("admin-groups", GroupViewSet)
router.register("admin-permissions", PermissionViewSet)


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/auth/", CustomAuthToken.as_view()),
    path("api/oauth/", CustomOAuthToken.as_view()),
    path("api/twilio/sms", twilio_webhooks.manejador_mensajes_entrantes),
    path("api/twilio/sms-error", twilio_webhooks.manejador_mensajes_error),
    path("api/", include(router.urls)),
    
    # Mercury API endpoints
    path("api/society/<str:society_id>/snapshot", society_snapshot, name="society_snapshot"),
    path("api/mercury/submit-onboarding-data", submit_onboarding_data, name="submit_onboarding_data"),
    path("api/mercury/webhooks", mercury_webhook, name="mercury_webhook"),
    path("api/society/<str:society_id>/mercury-status", mercury_status, name="mercury_status"),
    # path(
    #     "iq/contratos/subscription-agreements",
    #     subscription_agreements,
    #     name="subscription_agreements",
    # ),
    # path(
    #     "iq/contratos/subscription-agreements/<int:inversion_id>",
    #     subscription_agreements,
    #     name="subscription_agreements",
    # ),
    # path(
    #     "iq/contratos/offering-memorandum",
    #     subscription_agreements,
    #     name="subscription_agreements",
    # ),
    # path(
    #     "iq/contratos/offering-memorandum/<int:inversion_id>",
    #     subscription_agreements,
    #     name="offering_memorandum",
    # ),
    path(
        "spider/pagina-estatica/<codigo>", pagina_estatica_view, name="pagina_estatica"
    ),
    path("", home, name="home"),
    path('api/transferir-balance', TransferirBalanceView.as_view(), name='transferir-balance'),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls), prefix_default_language=False
)

