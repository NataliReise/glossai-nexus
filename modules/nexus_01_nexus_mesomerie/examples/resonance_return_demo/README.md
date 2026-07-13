# Public Resonance Return Demo

This directory contains a completely invented, public-safe walkthrough of the Nexus 01 local Resonance Return opening.

It does not contain personal configuration, private meaning, real participant data, or a real social connection.

## What the demo shows

```text
public-safe Resonance Return Artifact
-> copied local waiting slot
-> route and compatibility checks
-> local opening
   |- Resonance Artifact
   `- Nexus Echo
-> persistent Markdown result
-> slot state changes from waiting to opened
```

## Files

```text
resonance_return.demo.json   immutable public-safe return artifact
return_slots.template.json  immutable waiting-slot template
run_demo.py                  runner that creates mutable state elsewhere
```

The template files remain unchanged. Mutable slot state and the generated local result are written into a separate workspace.

## Run the demo

From the Nexus 01 module root:

```bash
python3 examples/resonance_return_demo/run_demo.py --reset
```

The default workspace is:

```text
/tmp/nexus-01-resonance-return-demo
```

The command prints the path of the generated Markdown result. Open that file to see both approved outputs.

## Run it again

```bash
python3 examples/resonance_return_demo/run_demo.py
```

The second run demonstrates:

```text
Generate once.
Revisit often.
```

The existing result is reused instead of overwritten, and the slot remains `opened`.

## Use another workspace

```bash
python3 examples/resonance_return_demo/run_demo.py \
  --workspace ~/tmp/nexus-resonance-demo \
  --reset
```

Choose a disposable or clearly local directory. The workspace contains a mutable slot document and a generated local result.

## Reset the default demo

Either run:

```bash
python3 examples/resonance_return_demo/run_demo.py --reset
```

or remove the workspace manually:

```bash
rm -rf /tmp/nexus-01-resonance-return-demo
```

## Expected Nexus Echo

```text
Summer rain
opens one hidden path
two feathers cross beneath waiting light
the path carries courage
trust
```

## Safety boundary

Everything in this demo is intentionally fictional and suitable for the public repository.

The demo does not:

- contact another person
- upload or synchronize data
- create a social graph
- expose private configuration
- infer meaning from free text
- call an AI or language model
- modify the immutable example files

## Working formula

```text
The public repository shows the path.
The private workspace carries the meaning.
```
