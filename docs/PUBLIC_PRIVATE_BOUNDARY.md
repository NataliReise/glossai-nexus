# Public / Private Boundary

This project is designed so that public modules can be shared without exposing private activation data.

## Public repository

The public repository may contain:

- module code
- public demo content
- placeholder configuration
- architecture notes
- documentation
- clearly marked example values

All example values must be unmistakably marked as public demo values.

Recommended placeholder patterns:

- `PUBLIC_DEMO_RESONANCE_CODE`
- `EXAMPLE_ACTIVATION_CODE_DO_NOT_USE`
- `SAMPLE_RETURN_CODE_DO_NOT_USE`
- `DEMO_ONLY_NOT_A_SECRET`

## Private activation layer

The private activation layer must not be committed to the public repository.

It may contain:

- real recipient names
- private gift messages
- personal configuration
- real activation codes
- real return codes
- personal notes
- contact data
- any credential, access token, password, private key, or API key

## Language rule for public examples

Public examples should avoid token-like or credential-like wording unless it is clearly part of a warning or documentation.

Avoid using realistic-looking values for:

- access tokens
- bearer tokens
- secrets
- private keys
- API keys
- activation keys
- return keys

Use clearly harmless placeholders instead.

## Core principle

The module may be public.
The activation remains private.
