from utils.classes.regex import Regex

SERIES_REGEXES = (
    Regex(showname="The Big Bang Theory",
          regex="((the.*)?big.?bang.?theory|T.?B.?B.?T|t.?b.?t[^a-z])"),

    Regex(showname="House M.D.",
          regex="(house(.?md)?|hse[^a-z]|h0u53|h.?s.?e.?[^a-z])"),

    Regex(showname="Two and a Half Men",
          regex="((two|2).?and.?a.?half.?men|t.?(a.)?a.?h.?m)"),

    Regex(showname="How I Met Your Mother",
          regex="(how.?i.?met.?your.?mother|h.?i.?m.?y.?m)"),

    Regex(showname="MythBusters",
          regex="mythbusters?"),

    Regex(showname="Futurama",
          regex="(futurama|fma[^a-z])"),

    Regex(showname="30 Rock",
          regex="(30|thirty).?rock"),

    Regex(showname="Top Gear",
          regex="((t.?gear|top.?g|.?top.?gear)|tg[^a-z])"),

    Regex(showname="Grey's Anatomy",
          regex="(greys.?anatomy|grys.?antmy|gry.?anatm|g\\.a[^a-z]|GA[^a-z]|grey.?s.?anatomy)"),

    Regex(showname="Breaking Bad",
          regex="(breaking.?bad|break.?bad|bb(s)?|brkng_bd)"),

    Regex(showname="Entourage",
          regex="(entourage|entrge)"),

    Regex(showname="Louie",
          regex="louie"),

    Regex(showname="Rome",
          regex="rome[^\\w]"),

    Regex(showname="Blue Mountain State",
          regex="blue.?mountain.?state"),

    Regex(showname="Its Always Sunny in Philadelphia",
          regex="(its.?)?always.?sunny.?(in.)?philadelphia"),

    Regex(showname="Weeds",
          regex="(weeds|we[^a-z]|wds)"),

    Regex(showname="Revenge",
          regex="(revenge|rvnge)"),

    Regex(showname="Lie To Me",
          regex="lie.?to.?me"),

    Regex(showname="Deadwood",
          regex="(deadwood|DDWD[^a-z])"),

    Regex(showname="The Walking Dead",
          regex="((the)?.?walking.?dead)"),

    Regex(showname="True Blood",
          regex="(true.?blood.|tr[^a-z]|txbx[^a-z])"),

    Regex(showname="The West Wing",
          regex="(the.)?west.?wing"),

    Regex(showname="Modern Family",
          regex="modern.?family"),

    Regex(showname="One Tree Hill",
          regex="(one.?th?ree.?hill|OTH[^a-z])"),

    Regex(showname="Person of Interest",
          regex="person.?of.?interest"),

    Regex(showname="Shameless",
          regex="(shameless|shmls[^a-z]|sham?[^a-z])"),

    Regex(showname="Terra Nova",
          regex="terra.?nova"),

    Regex(showname="Orange County",
          regex="(the.?o.?c.?|o\\.c[^a-z]|orange.?county)"),

    Regex(showname="Friends with Benefits",
          regex="fri(e|3)nds.?w(i|1)th.?b(e|3)n(e|3)f(i|1)ts?"),

    Regex(showname="OZ",
          regex="oz[^a-z]"),

    Regex(showname="Natholdet",
          regex="natholdet"),

    Regex(showname="Stand-up.dk",
          regex="stand.?up.?dk"),

    Regex(showname="Den Blinde Vinkel",
          regex="(den.?)?blinde.?vinkel"),

    Regex(showname="An Idiot Abroad",
          regex="(an.?)?idiot.?abroad"),

    Regex(showname="Blue Bloods",
          regex="blue.?bloods?"),

    Regex(showname="Game of Thrones",
          regex="game.?of.?thrones"),

    Regex(showname="Homeland",
          regex="(homeland|homel[^a-z])"),

    Regex(showname="Mad Men",
          regex="(mad.?men|md.?mn)"),

    Regex(showname="South Park",
          regex="south.?park"),

    Regex(showname="The Ricky Gervais Regex",
          regex="((the.?)?ricky.?gerva is.?Regex|trgs[^a-z])"),

    Regex(showname="Live at the Apollo",
          regex="(live.?(at.?)?(the.?)?apollo|lata[^a-z])"),

    Regex(showname="Pen and Teller - Bullshit",
          regex="penn.*teller.*bullshit"),

    Regex(showname="Community",
          regex="community"),

    Regex(showname="Cougar Town",
          regex="(cougar.?town|C.?T(s)?[^a-z]|cgr.?twn)"),

    Regex(showname="Awake",
          regex="awake"),

    Regex(showname="Skins",
          regex="skins"),

    Regex(showname="Suits",
          regex="(sts[^a-z]|suits)"),

    Regex(showname="Dragon Ball Z",
          regex="(dbz|dragon ball z)"),

    Regex(showname="Anger Management",
          regex="(anger.?management|^an.m[^a-z]|a\\.m[^a-z])"),

    Regex(showname="Arrested Development",
          regex="(arrested.?development)"),

    Regex(showname="Animal Practice",
          regex="(animal.?practice)"),

    Regex(showname="The Borgias",
          regex="borgias"),

    Regex(showname="Episodes",
          regex="episodes"),

    Regex(showname="The Newsroom",
          regex="the.?newsroom"),

    Regex(showname="Frozen Planet",
          regex="frozen.?planet"),

    Regex(showname="Wilfred",
          regex="wilfred"),

    Regex(showname="Parks and Recreation",
          regex="parks.?(and.)?recreation"),

    Regex(showname="Dexter",
          regex="dexter"),

    Regex(showname="Arrow",
          regex="arrow"),

    Regex(showname="Quite Interesting",
          regex="(qi xl|quite.?interesting)"),

    Regex(showname="Californication",
          regex="californication"),

    Regex(showname="The Shield",
          regex="the.?shield"),

    Regex(showname="Derek",
          regex="derek"),

    Regex(showname="House of Cards",
          regex="(house.?of.?cards|hos[^a-z])"),

    Regex(showname="Spartacus - War of the Damned",
          regex="spartacus(.*s03)?"),

    Regex(showname="New Girl",
          regex="new.?girl"),

    Regex(showname="Borgen",
          regex="borgen"),

    Regex(showname="Sons of Anarchy",
          regex="sons.?of.?anarchy"),

    Regex(showname="Hannibal",
          regex="(hannibal|hnb[^\w])"),

    Regex(showname="Continuum",
          regex="(continuum)"),

    Regex(showname="The IT Crowd",
          regex="(the)?.?it.?crowd"),
)
