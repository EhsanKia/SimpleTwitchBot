import random

faster = ["\"Let the games begin!\"", "\"Sweet Jesus!\"", "\"Not that!\"", "\"At last!\"",
	"\"Land o' Goshen!\"", "\"Is that all?\"", "\"Cheese it, the cops!\"",
	"\"I never dreamed it could be\"", "\"If I do, you won't respect me!\"", "\"Now!\"",
	"\"Open sesame!\"", "\"EMR!\"", "\"Again!\"", "\"Faster!\"", "\"Harder!\"", "\"Help!\"",
	"\"BOOM!!!, Headshot!\"", "\"Is it in yet?\"", "\"You aren't my father!\"",
	"\"Doctor, that's not *my* shoulder\"", "\"No, no, do the goldfish!\"",
	"\"Holy Batmobile, Batman!\"", "\"He's dead, he's dead!\"", "\"Take me, Robert!\"",
	"\"I'm a Republican!\"", "\"Put four fingers in!\"", "\"What a lover!\"",
	"\"Talk dirty, you pig!\"", "\"The ceiling needs painting,\"", "\"Suck harder!\"",
	"\"The animals will hear!\"", "\"Not in public!\""]
said = ["bellowed", "yelped", "croaked", "growled", "panted", "moaned", "grunted", "laughed",
	"warbled", "sighed", "ejaculated", "choked", "stammered", "wheezed", "squealed",
	"whimpered", "salivated", "tongued", "cried", "screamed", "yelled", "said"]
fadj = ["saucy", "wanton", "unfortunate", "lust-crazed", "nine-year-old", "bull-dyke", "bisexual",
	"gorgeous", "sweet", "nymphomaniacal", "large-hipped", "freckled", "forty-five year old",
	"white-haired", "large-boned", "saintly", "blind", "bearded", "blue-eyed", "large tongued",
	"friendly", "piano playing", "ear licking", "doe eyed", "sock sniffing", "lesbian", "hairy"]
female = ["baggage", "hussy", "woman", "Duchess", "female impersonator", "nymphomaniac", "virgin",
	"leather freak", "home-coming queen", "defrocked nun", "bisexual budgie", "cheerleader",
	"office secretary", "sexual deviate", "DARPA contract monitor", "little matchgirl",
	"ceremonial penguin", "femme fatale", "bosses' daughter", "construction worker",
	"sausage abuser", "secretary", "Congressman's page", "grandmother", "penguin",
	"German shepherd", "stewardess", "waitress", "prostitute", "computer science group",
	"housewife", "lady of the evening", "semen collector", "aviatrix", "burn victm"]
madj = ["thrashing", "slurping", "insatiable", "rabid", "satanic", "corpulent", "nose-grooming",
	"tripe-fondling", "dribbling", "spread-eagled", "orally fixated", "vile",
	"awesomely endowed", "handsome", "mush-brained", "tremendously hung", "three-legged",
	"pile-driving", "cross-dressing", "gerbil buggering", "bung-hole stuffing",
	"sphincter licking", "hair-pie chewing", "muff-diving", "clam shucking", "egg-sucking",
	"bicycle seat sniffing"]
male = ["rakehell", "hunchback", "lecherous lickspittle", "archduke", "midget", "hired hand",
	"great Dane", "stallion", "donkey", "electric eel", "paraplegic pothead",
	"dirty old man", "faggot butler", "friar", "black-power advocate", "follicle fetishist",
	"handsome priest", "chicken flicker", "homosexual flamingo", "ex-celibate", "drug sucker",
	"ex-woman", "construction worker", "hair dresser", "dentist", "judge",
	"social worker"]
diddled = ["diddled", "devoured", "fondled", "mouthed", "tongued", "lashed", "tweaked", "violated",
	"defiled", "irrigated", "soiled", "ravished", "hammered", "bit", "tongue slashed",
	"sucked", "rubbed", "masturbated with", "slurped"]
titadj = ["alabaster", "pink-tipped", "creamy", "rosebud", "moist", "throbbing", "juicy", "heaving",
	"straining", "mammoth", "succulent", "quivering", "rosey", "globular", "varicose",
	"jiggling", "bloody", "tilted", "dribbling", "oozing", "firm", "pendulous", "muscular",
	"bovine"]
knockers = ["globes", "melons", "mounds", "buds", "paps", "chubbies", "protuberances", "treasures",
	"buns", "bung", "vestibule", "armpits", "tits", "knockers", "elbows", "eyes", "hooters",
	"jugs", "lungs", "headlights", "disk drives", "bumpers", "knees", "fried eggs",
	"buttocks", "charlies", "ear lobes", "bazooms", "mammaries"]
and_word = ["and", "and then", "an'"]
thrust = ["plunged", "thrust", "squeezed", "pounded", "drove", "eased", "slid", "hammered",
	"squished", "crammed", "slammed", "reamed", "rammed", "dipped", "inserted", "plugged",
	"augured", "pushed", "ripped", "forced", "wrenched"]
dongadj = ["bursting", "jutting", "glistening", "Brobdingnagian", "prodigious", "purple", "searing",
	"swollen", "rigid", "rampaging", "warty", "steaming", "gorged", "trunklike",
	"foaming", "spouting", "swinish", "prosthetic", "blue veined", "engorged",
	"horse like", "throbbing", "humongous", "hole splitting", "serpentine", "curved",
	"steel encased", "glass encrusted", "knobby", "surgically altered", "metal tipped",
	"open sored", "rapidly dwindling", "swelling", "miniscule", "boney"]
dong = ["intruder", "prong", "stump", "member", "meat loaf", "majesty", "bowsprit", "earthmover",
	"jackhammer", "ramrod", "cod", "jabber", "gusher", "poker", "engine", "brownie",
	"joy stick", "plunger", "piston", "tool", "manhood", "lollipop", "kidney prodder",
	"candlestick", "John Thomas", "arm", "testicles", "balls", "finger", "foot", "tongue",
	"dick", "one-eyed wonder worm", "canyon yodeler", "middle leg", "neck wrapper",
	"stick shift", "dong", "Linda Lovelace choker"]
into = ["into", "right in", "inside"]
twatadj = ["pulsing", "hungry", "hymeneal", "palpitating", "gaping", "slavering", "welcoming",
	"glutted", "gobbling", "cobwebby", "ravenous", "slurping", "glistening", "dripping",
	"scabiferous", "porous", "soft-spoken", "pink", "dusty", "tight", "odiferous", "moist",
	"loose", "scarred", "weaponless", "banana-stuffed", "tire-tracked", "mouse-nibbled",
	"tightly-tensed", "oft-traveled", "grateful", "festering"]
twat = ["swamp", "honeypot", "jam jar", "butterbox", "furburger", "cherry pie", "cush", "slot",
	"slit", "cockpit", "damp", "furrow", "sanctum sanctorum", "bearded clam",
	"continental divide", "paradise valley", "red river valley", "slot machine", "quim",
	"palace", "areola", "rose bud", "throat", "eye socket", "tenderness", "inner ear",
	"orifice", "appendix scar", "wound", "navel", "mouth", "nose", "cunny"]

TEMPLATE = "{} {} {} as {} {} {} {} {} {} {} {} {} {} {} {} {} {}"


def gen_subject(sex=True):
	adjs, nouns = (madj, male) if sex else (fadj, female)
	noun = random.choice(nouns)
	adj = random.choice(adjs)
	return "the {} {}".format(adj, noun)


def sexytime(subject1=None, subject2=None, stype=1):
	if subject1 is None:
		subject1 = gen_subject(stype < 2)
	pronoun1 = "his" if stype < 2 else "a"

	if subject2 is None:
		subject2 = gen_subject(stype < 1)
		pronoun2 = "his" if stype < 1 else "her"
	else:
		pronoun2 = subject2 + "'s"

	params = []
	params.append(random.choice(faster))
	params.append(random.choice(said))
	params.append(subject2)
	params.append(subject1)
	params.append(random.choice(diddled))
	params.append(pronoun2)
	if stype < 1:
		params.append(random.choice(dongadj))
		params.append(random.choice(dong))
	else:
		params.append(random.choice(titadj))
		params.append(random.choice(knockers))
	params.append(random.choice(and_word))
	params.append(random.choice(thrust))
	params.append(pronoun1)
	params.append(random.choice(dongadj))
	params.append(random.choice(dong))
	params.append(random.choice(into))
	params.append(pronoun2)
	params.append(random.choice(twatadj))
	params.append(random.choice(twat))

	return TEMPLATE.format(*params)