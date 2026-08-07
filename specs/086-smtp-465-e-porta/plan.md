# Plano — spec 086

## Constitution Check

| Princípio | Conformidade |
|---|---|
| I — Evidência | A distinção 465/587 é verificável no código; a conclusão sobre egresso só se sustenta depois de eliminar a hipótese do transporte. |
| V — Segurança | `smtp_porta` é número de porta; senha e host continuam inacessíveis por qualquer rota. |
| VII — Spec-driven | Branch `086-smtp-465-e-porta`, merge `--no-ff`. |

## Arquivos

| Arquivo | Mudança |
|---|---|
| `chat-companion/backend/app.py` | `_abrir_smtp()` escolhe `SMTP_SSL` (465) ou `SMTP`+`starttls()`; `smtp_porta` no `/health`. |
| `chat-companion/backend/EMAIL.md` | Nota sobre a porta e o que fazer se o egresso estiver bloqueado. |

## Verificação

- `pytest` do backend.
- Contra produção: `/health` mostra a porta; `/assinar` entrega ou nomeia a falha.
