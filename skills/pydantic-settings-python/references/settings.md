# Settings source model

Built-in sources commonly include initializer arguments, environment variables,
dotenv files, secrets directories, and optional CLI input. Define environment
prefix, aliases, case sensitivity, nested delimiter, and complex-value decoding
as one external contract. A dotenv file is an input source, not a secret store.

Override `settings_customise_sources` only when the required priority differs
from documented defaults or a custom source is necessary. Return the complete
ordered tuple, then test every collision that matters. A custom source must
state its availability, error, precedence, decoding, and secret-handling policy.

Instantiate settings at startup. Pass the typed object to consumers rather than
having modules repeatedly inspect ambient environment state.
