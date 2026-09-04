# Public / Private Boundary

This project is designed so that public modules and public-safe carried content can be shared without exposing private activation or Return data.

## Public repository

The public repository may contain:

- module code
- public demo content
- public-safe built-in Archive Blocks and example Archive content
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

## Local public-safe carried content

A compatible data-only Archive Block may be deliberately coupled to a local Nexus.
That does not publish it externally, upload it, synchronize it, or make it part of a
travelling carrier automatically. Public-safe carried content remains distinct from private
Activation and Return history.

## Private local state

Private local state must not be committed to the public repository.

It may contain:

- real recipient names
- private gift messages
- personal configuration
- real activation codes
- selected Token context
- private Return Workspaces and Return Slots
- Return Artifacts and local Return Results
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

The module and public-safe Archive content may be public.
Private Activation and Return history remain private.
Nothing becomes public merely because it exists in a local Nexus.
