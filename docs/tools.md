# ForgeStack Tools

## Purpose

This document gives a stripped-down public-safe view of the current ForgeStack tool posture.

It exists to make four things explicit:

1. what ForgeStack is
2. what the active public tool is
3. what the current public model is
4. how reserved future lanes are represented without exposing private details

---

## Current tool posture

ForgeStack is the umbrella platform.

The active public CLI is:

- `devmake`

The canonical public model remains:

- stack
- app
- project
- output

The public repo should remain a complete, coherent free product on its own.

---

## Public tool stance

### Active public tool

- `devmake`

`devmake` is the current public command anchor and the normal public apply path.

### Reserved placeholders

The public repo may retain minimal reserved placeholders for future expansion:

- `devdata`
- `devview`

These placeholders should remain minimal and should not describe internal responsibilities, ownership maps, or private orchestration details.

---

## Public boundary rule

The public repo should:

- expose one normal public apply path
- describe only real public behavior
- avoid naming or documenting private orchestration paths
- avoid acting as a roadmap or blueprint for premium/internal lanes

The public repo should not:

- expose another visible apply path
- mirror private architecture just to reveal future seams
- add broad schema or command surface only to support private orchestration
- narrate hidden internal tool families in public docs

---

## Private boundary rule

The private repo remains separate.

Private depends on public.

Public never depends on private.

Private remains the place for richer orchestration, overlays, merge behavior, service wrappers, policy, and internal coordination value.

---

## Current implementation summary

Treat the current public stance as:

- ForgeStack is the umbrella platform
- `devmake` is the active public CLI
- the public repo is the clean public product lane
- minimal reserved placeholders may remain
- private orchestration details stay private

---

## Short summary

ForgeStack is the platform. `devmake` is the active public CLI. The canonical public model remains stack, app, project, and output. Minimal reserved placeholders may remain in public, but private orchestration details, ownership maps, and richer internal lane descriptions should stay out of the public repo.
