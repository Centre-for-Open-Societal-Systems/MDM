# syntax=docker/dockerfile:1

# ==============================================================================
# OpenAgriNet Master Data Management (MDM) - Catalog Registry Unified Dockerfile
# ==============================================================================
# Multi-stage build targets:
#   1. staff-api : FastAPI OpenG2P registry backend loaded with Catalog Extension & /v1 APIs
#   2. staff-ui  : Next.js OpenG2P staff portal web interface
#   3. db-seed   : Automated metadata seeding image
# ==============================================================================

ARG RP_VERSION=0.0.0-develop.384
ARG STAFF_UI_VERSION=1.1.1

# ---------------------------------------------------------------- staff API
FROM registry.gitlab.com/openg2p/registry/registry-platform/staff-api:${RP_VERSION} AS staff-api

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_catalog_extension

# Install Catalog Extension into Python environment
COPY catalog-extension/ /app/catalog-extension/
RUN pip install --no-cache-dir /app/catalog-extension

# Upstream platform patch for async intake policy condition
RUN python3 -c "\
import pathlib; \
p = pathlib.Path('/usr/local/lib/python3.12/site-packages/openg2p_registry_core/services/intake_form_data_service.py'); \
s = p.read_text(); \
old = '    def _build_intake_policy_condition('; \
new = '    async def _build_intake_policy_condition('; \
assert s.count(old) == 1, f'expected exactly one match, found {s.count(old)}'; \
p.write_text(s.replace(old, new))"

# ----------------------------------------------------------------- staff UI
FROM openg2p/openg2p-registry-staff-portal-ui:${STAFF_UI_VERSION} AS staff-ui

# Prefer human-readable form descriptions in UI navigation
RUN find /app/.next -type f -name '*.js' -exec sed -i \
    -e 's/title:e\.form_mnemonic,children:e\.form_mnemonic/title:e.form_description||e.form_mnemonic,children:e.form_description||e.form_mnemonic/g' \
    -e 's/form_name:\([A-Za-z_$][A-Za-z0-9_$]*\)[?]\.form_mnemonic/form_name:\1?.form_description||\1?.form_mnemonic/g' \
    -e 's/form_name:\([A-Za-z_$][A-Za-z0-9_$]*\)\.form_mnemonic/form_name:\1.form_description||\1.form_mnemonic/g' \
    {} +

# Display all configured detail tabs directly without hiding in overflow
RUN find /app/.next -type f -name '*.js' -exec sed -i \
    's/k=S\.slice(0,5),A=S\.slice(5)/k=S,A=[]/g' \
    {} +

# Prevent Filter Dialog crashes and default operators gracefully
RUN find /app/.next -type f -name '*.js' -exec sed -i \
    -e 's/E=void 0===A?\[\]:A/E=Array.isArray(A)?A:[]/g' \
    -e 's/i=f??\[\]/i=Array.isArray(f)?f:[]/g' \
    -e 's/c=r??\[\]/c=Array.isArray(r)?r:[]/g' \
    -e 's/j=c??\[\]/j=Array.isArray(c)?c:[]/g' \
    -e 's/t\.find(t=>t\.register_id===e)/(Array.isArray(t)?t.find(t=>t.register_id===e):undefined)/g' \
    -e 's/t\.find(t=>t\.tab_id===e)/(Array.isArray(t)?t.find(t=>t.tab_id===e):undefined)/g' \
    -e 's/y=eo\.map(e)/y=Array.isArray(eo)?eo.map(e):[]/g' \
    -e 's/H&&L("")/H\&\&L(H.allowed_operators?.[0]||"")/g' \
    -e 's/if(!H||!W)return;let e={field_name:H\.field_name,operator:W,value:M}/let op=W||H?.allowed_operators?.[0]||"";if(!H||!op)return;let e={field_name:H.field_name,operator:op,value:M}/g' \
    {} +

# ------------------------------------------------------------------ DB seed
FROM registry.gitlab.com/openg2p/registry/registry-platform/db-seed:${RP_VERSION} AS db-seed

RUN rm -rf /seed/meta_data/* /seed/awe_meta_data/* /seed/templates/* /seed/seed-data/*

COPY catalog-extension/src/openg2p_registry_catalog_extension/meta_data/ /seed/meta_data/
