# Lógica de cálculo

- v28 = unidades vendidas 28 d / 28 ; v90 = unidades 90 d / 90
- v_cuando = max(v28, v90) ; v_cuanto = 0.6·v28 + 0.4·v90
- Posible quiebre: disponible ≤ 0 y v28 = 0 y v90 > 0 → v_cuanto = v90
- cobertura_dias = (disponible + tránsito + borradores) / v_cuando
- objetivo = pendientes_cliente + v_cuanto × cobertura_objetivo (45 días; el lead time y la seguridad solo deciden CUÁNDO pedir, no CUÁNTO)
- sugerido = ceil((objetivo − disponible − tránsito − borradores) / múltiplo) × múltiplo ; si < MOQ → MOQ
- Entra al pedido si cobertura_dias < lead_time + seguridad + horizonte_revision
- Lento: v90 > 0 y cobertura > sobrestock_dias → exceso = disponible − v_cuanto×sobrestock_dias
- Muerto: v90 = 0 y disponible > 0 → capital = disponible × costo estándar
- Atípica: un solo cliente > 50% de unidades 90 d (y > 20 u) → alerta, no se excluye
- Marca: brand_id → x_studio_marca → x_studio_brand_vg → primera palabra del nombre (mayúsculas)
- Borradores abiertos de otras semanas se restan para no duplicar; los de la semana actual se reemplazan (paso 2)
