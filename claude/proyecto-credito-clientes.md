# Proyecto: autorización de crédito para clientes nuevos (Ventas Guate)

Estado al **2026-11-28**: diseño propuesto; **pendiente de decisiones de política de Diego**. No se ha construido nada en Odoo todavía.
Responsables: Diego Segura (decide la política y los textos legales), Glenda Ixcayau (contabilidad / aprobación), Henry Galindo (gerente de distribución / aprobación).

## 1. Objetivo
Automatizar la solicitud, evaluación, aprobación y formalización del crédito a clientes nuevos y la revisión periódica de los existentes:
- Formulario en línea que el cliente llena y que deja el expediente guardado en Odoo.
- Dictamen automático: viabilidad, calificación, límite y plazo sugeridos.
- Aprobación por monto.
- Firma de los documentos de obligación.
- El crédito se activa en Odoo solo cuando todo está completo.

## 2. Lo que ya existe en Odoo (verificado 2026-11-27)
- **`base.automation` 11 "Crédito: bloqueo al confirmar pedido"** (acción `ir.actions.server` 1648). Al confirmar un `sale.order` lo bloquea si:
  - el cliente tiene facturas vencidas de más de 5 días, o
  - su exposición supera `credit_limit` (con `use_partner_credit_limit` activo). Exposición = cartera (`credit`) + pedidos por facturar de los últimos 90 días + consignación a precio de lista (`x_consig_location_ids`) + el pedido.
- **`base.automation` 12 "Crédito: liberación solo autorizada"**: el campo `x_credito_liberado` del pedido solo lo pueden marcar Diego (2), Glenda (27) y Henry (7).
- Solo **30 clientes** tienen límite (`use_partner_credit_limit`), de Q1,000 a Q1,500,000, sin criterio uniforme.
- Plazos de pago de los clientes con límite o con saldo:

  | Plazo | Clientes |
  |---|---|
  | 30 días | 26 |
  | 2 días | 15 |
  | Sin plazo | 10 |
  | 8 días | 5 |
  | 20 días | 1 |
  | 45 días | 1 |
  | 2 meses | 1 |
- Comportamiento de pago, promedio de días de atraso sobre facturas pagadas en 12 meses (ejemplos):

  | Cliente | Días de atraso promedio |
  |---|---|
  | ISHOP | 16 |
  | GYKS | 17 |
  | MOKA | 24 |
  | OTTOS | 19 |
  | OBITECH | 1 |
  | TRAVELSHOP | 8 |
  | PACIFIKO.COM | −3 |
  | SMARTSONIC | −15 (paga antes) |
- Módulos instalados que se usarán: **website** (formulario público), **documents** (expediente), **sign** + **documents_sign** (firma electrónica), **approvals** (flujo de aprobación), **survey**, **portal**, **account_followup**, **l10n_gt_edi**.

## 3. Flujo propuesto
| Paso | Quién | Qué hace |
|---|---|---|
| 1. Solicitud | Vendedor envía enlace; el cliente llena | Página "Solicitud de crédito" en el sitio Odoo. Pide datos (NIT, razón social, años operando, tipo de cliente: cadena/mayorista/tienda/plataforma, compra mensual esperada, plazo solicitado, 2 referencias comerciales, 1 bancaria, garantía ofrecida) y la carga de documentos |
| 2. Registro | Automático | Crea solicitud en **Aprobaciones** ligada al `res.partner`; archivos a **Documentos → Crédito → [Cliente]** |
| 3. Revisión automática | Odoo | NIT duplicado o de parte relacionada; historial de compras de contado (montos, frecuencia, días de pago); cartera vencida en otro contacto del mismo NIT; documentos completos |
| 4. Dictamen | Odoo | Calificación A/B/C/D, límite y plazo sugeridos y condición de arranque (p. ej. primeros 3 pedidos de contado o 50% de anticipo) |
| 5. Aprobación | Según monto | Actividad al aprobador correspondiente |
| 6. Formalización | Automático + físico | Envío a firma (Odoo Sign) y registro del pagaré físico. **El crédito no se activa hasta tener todas las firmas** |
| 7. Activación | Automático | Escribe `credit_limit`, `use_partner_credit_limit`, plazo de pago y nota con el dictamen; el bloqueo existente (automatización 11) empieza a aplicar |
| 8. Revisión mensual | Rutina | Recalifica a los clientes con crédito por su pago real; sugiere subir, bajar o congelar el límite |

### Fórmula propuesta (a confirmar)
- **Límite base** = compra mensual esperada × (plazo en días ÷ 30 + 0.5), con tope según la calificación.
- **Tope para cliente nuevo:**

  | Calificación | Tope |
  |---|---|
  | A | Q150K |
  | B | Q50K |
  | C | Q15K |
  | D | Solo contado |
- **Aumento sugerido:** después de 3 meses con atraso promedio de 5 días o menos, +50%.

## 4. Documentos de soporte propuestos
| Documento | S.A. | Individual | Cuándo |
|---|---|---|---|
| RTU actualizado | ✓ | ✓ | Siempre |
| Patente de comercio (empresa; y de sociedad en S.A.) | ✓ | ✓ | Siempre |
| Nombramiento del representante legal inscrito | ✓ | — | Siempre |
| DPI del representante o propietario | ✓ | ✓ | Siempre |
| Recibo de servicio del local | ✓ | ✓ | Siempre |
| 2 referencias comerciales y 1 bancaria (o estados de cuenta de 3 meses) | ✓ | ✓ | Siempre |
| Autorización de consulta a buró | ✓ | ✓ | Siempre |
| Estados financieros del último año | ✓ | Opcional | Límite > Q50K |
| Declaración de IVA o ISR del último año | ✓ | ✓ | Límite > Q50K |
| Foto del local | ✓ | ✓ | Sin historial |
| Contrato o condiciones de crédito firmadas | ✓ | ✓ | Siempre |
| Pagaré | ✓ | ✓ | Según monto |

## 5. Firma y garantías (propuesta)
| Límite aprobado | Documentos |
|---|---|
| Hasta Q15K | Contrato o condiciones de crédito, autorización de buró y declaración de veracidad, con **firma electrónica (Odoo Sign)** |
| De Q15K a Q75K | Lo anterior + **pagaré físico** firmado por el representante (escaneado al expediente y marcado como recibido) |
| Más de Q75K | Lo anterior + pagaré con **firma legalizada** + **aval personal** del socio o representante |

Nota legal, a criterio de Diego como abogado:
- Firma electrónica simple: válida bajo el Decreto 47-2008.
- Para cobrar el pagaré por vía ejecutiva conviene el original con firma autógrafa o firma electrónica avanzada certificada.

## 6. Decisiones pendientes (Diego)
1. **Aprobadores por monto.** Propuesta: hasta Q15K Henry · de Q15K a Q75K Henry y Glenda · más de Q75K Diego.
2. **Plazo máximo para nuevos.** Propuesta: 15 días tiendas y mayoristas, 30 días cadenas.
3. **Garantía por monto.** Propuesta: la tabla de la sección 5.
4. **Criterios que descalifican.** Ejemplos: menos de 1 año operando, sin RTU, referencias negativas, NIT con cartera vencida.
5. **Textos legales:** contrato o condiciones de crédito, pagaré, autorización de buró, declaración de veracidad y aval. ¿Los redacta Diego o se le prepara un borrador?
6. **Buró de crédito:** ¿Infornet, TransUnion o Crediref? ¿Tiene API?
7. **Clientes actuales con crédito:** ¿regularizarlos (contrato y pagaré) en 60 días?
8. **Dónde publicar el formulario:** página en el sitio Odoo (ventasguate.odoo.com) o enlazada desde ventasguate.gt.

## 7. Plan de construcción (después de las decisiones)
1. Campos y modelo de la solicitud: Aprobaciones (categoría "Crédito cliente") + campos de evaluación.
2. Formulario web con carga de archivos → solicitud + carpeta en Documentos.
3. Acción de servidor "Evaluar crédito": revisión automática + dictamen.
4. Reglas de aprobación por monto y actividades.
5. Plantillas en Odoo Sign; activación del crédito al completar las firmas.
6. Rutina mensual de recalificación (solo lectura + propuesta; los cambios de límite los aprueba Diego, Glenda o Henry).
7. Prueba con 3 clientes reales (uno bueno, uno regular y uno malo) antes de abrirlo a los vendedores.

**Reglas del proyecto:**
- Odoo solo lectura salvo instrucción explícita.
- Respaldo antes de cambiar configuración (`odoo-audit/respaldos/`).
- No tocar los permisos de María Fernanda (15).

## 8. Cómo retomarlo en otro chat
Pegar:
> Retomemos el proyecto de crédito para clientes nuevos de Ventas Guate. Lee `claude/proyecto-credito-clientes.md` y CLAUDE.md del repo Dsegurav203/Ventas-Guate. Estas son mis decisiones sobre la sección 6: … Empieza por el paso 1 del plan.
