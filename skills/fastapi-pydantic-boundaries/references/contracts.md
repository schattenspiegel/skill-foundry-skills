# Request and response contracts

Map each value to path, query, header, cookie, body, form, or file. Distinguish
input aliases from serialized output names. Use discriminated unions for tagged
bodies. Response models are allowlists; design them explicitly and test OpenAPI
plus actual JSON. Partial update semantics require missing versus explicit null.
