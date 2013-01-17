MOD_GROUPS = set(['globalmod', 'mod', 'mod2', 'mod3'])

# Ranking for moderators.
# This allows us to do a simple less than/greater than to evaluate permissions.
GROUP_RANKS = {
    'globalmod': 6,
    'mod': 5,
    'mod2': 4,
    'mod3': 3,
    'user': 2,
    'silent': 1,
}

# Just how high do you even have to be to do that?
MINIMUM_RANKS = {
    'ip_ban': 5,
    'kick': 4,
}

