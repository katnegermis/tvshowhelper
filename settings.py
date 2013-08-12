import re
import os

from utils.classes.regex import Regex


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

SEASON_EPISODE_REGEX = re.compile("(s|se|season)(?P<season>\d{1,2})(e|ep|episode)(?P<episode>\d{1,2})", re.IGNORECASE)
SEASON_EPISODE_REGEX_NASTY = re.compile("((?P<season>\d{1,2})(?P<episode>\d{1,2}))(?!(p|mb))", re.IGNORECASE)

IF_NOT_SHOW_EXISTS_CREATE_FOLDER = True

VIDEO_COMMAND = "vlc"

# SERIES_ROOT_FOLDER = "/media/server_storage/film/Serier"
SERIES_ROOT_FOLDER = "/media/server_storage/film/Serier"

CACHE_FILE = os.path.join(ROOT_DIR, "data", "cache.json")

SERIES_REGEXES = [
    Regex(name="The Big Bang Theory",
          regex="((the.*)?big.?bang.?theory|T.?B.?B.?T|t.?b.?t[^a-z])"),

    Regex(name="House M.D.",
          regex="(house(.?md)?|hse[^a-z]|h0u53|h.?s.?e.?[^a-z])"),

    Regex(name="Two and a Half Men",
          regex="((two|2).?and.?a.?half.?men|t.?(a.)?a.?h.?m)"),

    Regex(name="How I Met Your Mother",
          regex="(how.?i.?met.?your.?mother|h.?i.?m.?y.?m)"),

    Regex(name="MythBusters",
          regex="mythbusters?"),

    Regex(name="Futurama",
          regex="(futurama|fma[^a-z])"),

    Regex(name="30 Rock",
          regex="(30|thirty).?rock"),

    Regex(name="Top Gear",
          regex="((t.?gear|top.?g|.?top.?gear)|tg[^a-z])"),

    Regex(name="Grey's Anatomy",
          regex="(greys.?anatomy|grys.?antmy|gry.?anatm|g\\.a[^a-z]|GA[^a-z]|grey.?s.?anatomy)"),

    Regex(name="Breaking Bad",
          regex="(breaking.?bad|break.?bad|bb(s)?|brkng_bd)"),

    Regex(name="Entourage",
          regex="(entourage|entrge)"),

    Regex(name="Louie",
          regex="louie"),

    Regex(name="Rome",
          regex="rome[^\\w]"),

    Regex(name="Blue Mountain State",
          regex="blue.?mountain.?state"),

    Regex(name="Its Always Sunny in Philadelphia",
          regex="(its.?)?always.?sunny.?(in.)?philadelphia"),

    Regex(name="Weeds",
          regex="(weeds|we[^a-z]|wds)"),

    Regex(name="Revenge",
          regex="(revenge|rvnge)"),

    Regex(name="Lie To Me",
          regex="lie.?to.?me"),

    Regex(name="Deadwood",
          regex="(deadwood|DDWD[^a-z])"),

    Regex(name="The Walking Dead",
          regex="((the)?.?walking.?dead)"),

    Regex(name="True Blood",
          regex="(true.?blood.|tr[^a-z]|txbx[^a-z])"),

    Regex(name="The West Wing",
          regex="(the.)?west.?wing"),

    Regex(name="Modern Family",
          regex="modern.?family"),

    Regex(name="One Tree Hill",
          regex="(one.?th?ree.?hill|OTH[^a-z])"),

    Regex(name="Person of Interest",
          regex="person.?of.?interest"),

    Regex(name="Shameless",
          regex="(shameless|shmls[^a-z]|sham?[^a-z])"),

    Regex(name="Terra Nova",
          regex="terra.?nova"),

    Regex(name="Orange County",
          regex="(the.?o.?c.?|o\\.c[^a-z]|orange.?county)"),

    Regex(name="Friends with Benefits",
          regex="fri(e|3)nds.?w(i|1)th.?b(e|3)n(e|3)f(i|1)ts?"),

    Regex(name="OZ",
          regex="oz[^a-z]"),

    Regex(name="Natholdet",
          regex="natholdet"),

    Regex(name="Stand-up.dk",
          regex="stand.?up.?dk"),

    Regex(name="Den Blinde Vinkel",
          regex="(den.?)?blinde.?vinkel"),

    Regex(name="An Idiot Abroad",
          regex="(an.?)?idiot.?abroad"),

    Regex(name="Blue Bloods",
          regex="blue.?bloods?"),

    Regex(name="Game of Thrones",
          regex="game.?of.?thrones"),

    Regex(name="Homeland",
          regex="(homeland|homel[^a-z])"),

    Regex(name="Mad Men",
          regex="(mad.?men|md.?mn)"),

    Regex(name="South Park",
          regex="south.?park"),

    Regex(name="The Ricky Gervais Regex",
          regex="((the.?)?ricky.?gerva is.?Regex|trgs[^a-z])"),

    Regex(name="Live at the Apollo",
          regex="(live.?(at.?)?(the.?)?apollo|lata[^a-z])"),

    Regex(name="Pen and Teller - Bullshit",
          regex="penn.*teller.*bullshit"),

    Regex(name="Community",
          regex="community"),

    Regex(name="Cougar Town",
          regex="(cougar.?town|C.?T(s)?[^a-z]|cgr.?twn)"),

    Regex(name="Awake",
          regex="awake"),

    Regex(name="Skins",
          regex="skins"),

    Regex(name="Suits",
          regex="(sts[^a-z]|suits)"),

    Regex(name="Dragon Ball Z",
          regex="(dbz|dragon ball z)"),

    Regex(name="Anger Management",
          regex="(anger.?management|^an.m[^a-z]|a\\.m[^a-z])"),

    Regex(name="Arrested Development",
          regex="(arrested.?development)"),

    Regex(name="Animal Practice",
          regex="(animal.?practice)"),

    Regex(name="The Borgias",
          regex="borgias"),

    Regex(name="Episodes",
          regex="episodes"),

    Regex(name="The Newsroom",
          regex="the.?newsroom"),

    Regex(name="Frozen Planet",
          regex="frozen.?planet"),

    Regex(name="Wilfred",
          regex="wilfred"),

    Regex(name="Parks and Recreation",
          regex="parks.?(and.)?recreation"),

    Regex(name="Dexter",
          regex="dexter"),

    Regex(name="Arrow",
          regex="arrow"),

    Regex(name="Quite Interesting",
          regex="(qi xl|quite.?interesting)"),

    Regex(name="Californication",
          regex="californication"),

    Regex(name="The Shield",
          regex="the.?shield"),

    Regex(name="Derek",
          regex="derek"),

    Regex(name="House of Cards",
          regex="(house.?of.?cards|hos[^a-z])"),

    Regex(name="Spartacus - War of the Damned",
          regex="spartacus(.*s03)?"),

    Regex(name="New Girl",
          regex="new.?girl"),

    Regex(name="Borgen",
          regex="borgen"),

    Regex(name="Sons of Anarchy",
          regex="sons.?of.?anarchy"),

    Regex(name="Hannibal",
          regex="(hannibal|hnb[^\w])"),
]
