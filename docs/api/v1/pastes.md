# Pastes
Contains views for interacting with pastes.

## GET /v1/pastes/
**AUTH REQUIRED**

Returns all user's pastes

## POST /v1/pastes/
Creates new paste.

## GET /v1/pastes/<paste_hash>/
Returns info about paste with <paste_hash>.

## DELETE /v1/pastes/<paste_hash>/
**AUTH REQUIRED**, **OWNERSHIP REQURED**

Deletes paste with <paste_hash>.

## PATCH /v1/pastes/<paste_hash>/
**AUTH REQUIRED**, **OWNERSHIP REQURED**

Edits text or language of paste with <paste_hash>.

## GET /v1/pastes/<paste_hash>/stats
**STATS ACCESS REQURED**

Returns statistics of paste with <paste_hash>.

## DELETE /v1/pastes/<paste_hash>/stats
**AUTH REQUIRED**, **OWNERSHIP REQURED**

Cleares paste statistics with <paste_hash>.
