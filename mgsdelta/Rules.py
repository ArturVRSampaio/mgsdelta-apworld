"""
Access rules (region entrances + location requirements) for MGS Delta.

TODO: encode things like:
  - "reaching The End's fight requires thermal goggles" (or logic-approved
    alternative strategies, if we decide to support the cardboard-box/
    save-and-quit skip as an option).
  - "opening storage door X requires key item Y".

Keep rules 1:1 with what mgsdelta-connector can actually verify a player owns
at runtime — don't add a rule for an item the connector can't grant/detect yet.
"""
