# Ownership and errors

Dependencies own request-scoped resources; lifespan owns application-scoped
resources. Convert expected domain failures to documented HTTP errors. Preserve
unexpected defects for server observability. Never perform I/O in validators or
serialize raw settings, ORM state, or exception objects into responses.
