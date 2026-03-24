import json
import random
import uuid
from pathlib import Path


OUTPUT_PATH = Path(__file__).with_name("medical_knowledge.json")
MIN_NEW_ENTRIES = 400
MAX_NEW_ENTRIES = 500
MIN_WORDS = 100
MAX_WORDS = 300


TOPIC_FOCUSES = {
	"diabetes": [
		"blood glucose control",
		"type 1 and type 2 distinctions",
		"preventing long-term complications",
		"lifestyle and medication adherence",
	],
	"cancer": [
		"screening and early detection",
		"evidence-based treatment planning",
		"risk factor reduction",
		"multidisciplinary oncology care",
	],
	"heart disease": [
		"atherosclerosis prevention",
		"cholesterol and blood pressure management",
		"recognizing heart attack warning signs",
		"long-term cardiovascular risk reduction",
	],
	"hypertension": [
		"silent nature of high blood pressure",
		"kidney and heart protection",
		"salt reduction and lifestyle therapy",
		"long-term medication adherence",
	],
	"vaccines": [
		"community protection through immunization",
		"vaccine safety monitoring",
		"routine immunization schedules",
		"preventing severe infectious disease",
	],
	"mental health": [
		"depression and anxiety treatment",
		"reducing stigma and improving access",
		"crisis warning signs",
		"evidence-based psychotherapy and medicines",
	],
	"nutrition": [
		"balanced dietary patterns",
		"micronutrient adequacy",
		"diet and chronic disease prevention",
		"healthy eating across the lifespan",
	],
	"obesity": [
		"long-term weight management",
		"metabolic risk reduction",
		"behavioral support and physical activity",
		"medical management for severe obesity",
	],
	"supplements": [
		"safe use of vitamins and minerals",
		"drug-supplement interactions",
		"evidence quality for common supplements",
		"risks of megadoses",
	],
	"infectious diseases": [
		"preventing transmission",
		"antimicrobial stewardship",
		"early diagnosis and isolation",
		"public health response principles",
	],
	"pregnancy": [
		"antenatal care and screening",
		"maternal nutrition and supplementation",
		"warning signs requiring urgent review",
		"safe medication use in pregnancy",
	],
	"child health": [
		"growth and developmental surveillance",
		"childhood immunization",
		"nutrition and infection prevention",
		"early recognition of serious illness",
	],
}


SOURCES = {
	"diabetes": [
		("WHO Diabetes Fact Sheet", "https://www.who.int/news-room/fact-sheets/detail/diabetes"),
		("CDC Diabetes Basics", "https://www.cdc.gov/diabetes/basics/diabetes.html"),
		("NHS Type 2 Diabetes", "https://www.nhs.uk/conditions/type-2-diabetes/"),
	],
	"cancer": [
		("WHO Cancer Fact Sheet", "https://www.who.int/news-room/fact-sheets/detail/cancer"),
		("NHS Cancer Overview", "https://www.nhs.uk/conditions/cancer/"),
		("CDC Cancer Prevention", "https://www.cdc.gov/cancer/dcpc/prevention/index.htm"),
	],
	"heart disease": [
		(
			"WHO Cardiovascular Diseases Fact Sheet",
			"https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds)",
		),
		("CDC Heart Disease", "https://www.cdc.gov/heartdisease/index.htm"),
		("NHS Coronary Heart Disease", "https://www.nhs.uk/conditions/coronary-heart-disease/"),
	],
	"hypertension": [
		("WHO Hypertension Fact Sheet", "https://www.who.int/news-room/fact-sheets/detail/hypertension"),
		(
			"CDC High Blood Pressure",
			"https://www.cdc.gov/high-blood-pressure/about/index.html",
		),
		(
			"NHS High Blood Pressure Overview",
			"https://www.nhs.uk/conditions/high-blood-pressure-hypertension/",
		),
	],
	"vaccines": [
		("WHO Vaccine Safety", "https://www.who.int/news-room/fact-sheets/detail/vaccine-safety"),
		("CDC Vaccine Safety", "https://www.cdc.gov/vaccinesafety/index.html"),
		("NHS Vaccinations", "https://www.nhs.uk/conditions/vaccinations/"),
	],
	"mental health": [
		("WHO Mental Health", "https://www.who.int/health-topics/mental-health"),
		("NHS Mental Health Services", "https://www.nhs.uk/mental-health/"),
		("CDC Mental Health", "https://www.cdc.gov/mentalhealth/index.htm"),
	],
	"nutrition": [
		("WHO Healthy Diet", "https://www.who.int/news-room/fact-sheets/detail/healthy-diet"),
		("NHS Eat Well", "https://www.nhs.uk/live-well/eat-well/"),
		(
			"CDC Nutrition, Physical Activity, and Obesity",
			"https://www.cdc.gov/nutrition/index.html",
		),
	],
	"obesity": [
		("WHO Obesity and Overweight", "https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight"),
		("CDC Adult Obesity Facts", "https://www.cdc.gov/obesity/data/adult.html"),
		("NHS Obesity", "https://www.nhs.uk/conditions/obesity/"),
	],
	"supplements": [
		("NHS Vitamins and Minerals", "https://www.nhs.uk/conditions/vitamins-and-minerals/"),
		(
			"NIH Office of Dietary Supplements",
			"https://ods.od.nih.gov/factsheets/list-all/",
		),
		("CDC Nutrition Resources", "https://www.cdc.gov/nutrition/resources-publications/index.html"),
	],
	"infectious diseases": [
		(
			"WHO Infectious Hazards Management",
			"https://www.who.int/teams/health-emergencies-programme/infectious-hazards-management",
		),
		(
			"CDC Infectious Diseases",
			"https://www.cdc.gov/ncezid/index.html",
		),
		(
			"NHS Infections and Antibiotics",
			"https://www.nhs.uk/conditions/antibiotics/",
		),
	],
	"pregnancy": [
		("WHO Maternal Health", "https://www.who.int/health-topics/maternal-health"),
		("NHS Pregnancy", "https://www.nhs.uk/pregnancy/"),
		(
			"CDC Pregnancy and Maternal Health",
			"https://www.cdc.gov/reproductive-health/maternal-infant-health/pregnancy.html",
		),
	],
	"child health": [
		("WHO Child Health", "https://www.who.int/health-topics/child-health"),
		("NHS Health A to Z for Children", "https://www.nhs.uk/conditions/baby/"),
		(
			"CDC Child Development",
			"https://www.cdc.gov/ncbddd/childdevelopment/index.html",
		),
	],
}


TOPIC_FACTS = {
	"diabetes": [
		"Diabetes is a chronic metabolic condition characterized by elevated blood glucose due to insulin deficiency, insulin resistance, or both.",
		"Type 1 diabetes requires lifelong insulin therapy because the pancreas produces little or no insulin.",
		"Type 2 diabetes can often be delayed or better controlled through diet quality, physical activity, weight management, and medication when needed.",
		"Long-term uncontrolled glucose increases the risk of kidney disease, nerve damage, vision loss, heart disease, and stroke.",
		"Routine monitoring of blood glucose and glycated hemoglobin helps clinicians adjust treatment safely.",
		"Medication changes should be supervised by a licensed clinician to avoid hypoglycemia and treatment failure.",
	],
	"cancer": [
		"Cancer includes many diseases in which abnormal cells grow uncontrollably and can invade nearby tissues or spread to distant organs.",
		"Early detection through screening improves outcomes for several cancers because treatment can begin before advanced spread.",
		"Main treatment options include surgery, radiotherapy, systemic therapy, and supportive care, selected by cancer type and stage.",
		"Tobacco exposure, alcohol misuse, obesity, and some infections increase risk, while prevention strategies can lower population burden.",
		"Multidisciplinary teams coordinate care plans to balance survival benefit, quality of life, and side-effect management.",
		"Unproven alternative remedies should not replace oncologist-directed treatment because delays can worsen prognosis.",
	],
	"heart disease": [
		"Heart disease commonly develops through atherosclerosis, where fatty plaques narrow arteries and reduce blood flow to the heart muscle.",
		"High blood pressure, high LDL cholesterol, diabetes, smoking, and physical inactivity are major modifiable risk factors.",
		"Warning signs of acute coronary syndrome include chest pressure, breathlessness, sweating, and pain radiating to arm or jaw.",
		"Evidence-based prevention combines smoking cessation, healthy diet patterns, regular exercise, and prescribed medicines when indicated.",
		"Statins and blood pressure treatments reduce cardiovascular events in high-risk patients when taken consistently.",
		"Rapid emergency care during heart attack improves survival and reduces permanent heart damage.",
	],
	"hypertension": [
		"Hypertension often has no obvious symptoms, which is why regular blood pressure checks are essential.",
		"Persistently elevated blood pressure damages blood vessels and increases risk of stroke, heart attack, kidney disease, and heart failure.",
		"Lifestyle interventions include reducing sodium, maintaining healthy weight, limiting alcohol, and increasing physical activity.",
		"Many patients need long-term medication because lifestyle measures alone may not achieve target blood pressure.",
		"Adherence is important because stopping antihypertensives can lead to uncontrolled pressure and acute complications.",
		"Home blood pressure monitoring can improve treatment adjustments when readings are measured correctly.",
	],
	"vaccines": [
		"Vaccines train the immune system to recognize harmful pathogens and reduce the risk of severe illness, hospitalization, and death.",
		"Licensed vaccines undergo phased clinical trials followed by post-marketing safety surveillance.",
		"Common side effects are usually mild and short-lived, such as soreness, fatigue, or low-grade fever.",
		"High community vaccination coverage helps protect people who cannot be vaccinated because of medical contraindications.",
		"Immunization schedules are designed to provide protection at ages when risk from infections is highest.",
		"Misinformation about infertility, autism, or implanted tracking devices is not supported by high-quality scientific evidence.",
	],
	"mental health": [
		"Mental health conditions are real medical disorders influenced by biological, psychological, and social factors.",
		"Depression, anxiety, bipolar disorder, and psychotic disorders can be treated effectively with tailored care plans.",
		"Evidence-based therapies include psychological interventions, medication, social support, and crisis services when needed.",
		"Early treatment reduces disability and lowers risk of self-harm, substance misuse, and social isolation.",
		"Stigma can delay care, so supportive communication and timely referral are essential in primary and community settings.",
		"Abruptly stopping psychiatric medication without supervision may trigger relapse or withdrawal symptoms.",
	],
	"nutrition": [
		"Nutrition supports growth, immune function, metabolism, and long-term prevention of chronic disease.",
		"Balanced diets emphasize vegetables, fruits, legumes, whole grains, lean protein sources, and unsaturated fats.",
		"Limiting excess sodium, free sugars, and highly processed foods helps lower cardiometabolic risk.",
		"Hydration, food safety, and regular meal patterns are practical components of healthy eating guidance.",
		"Nutritional plans should consider age, cultural preferences, medical conditions, and economic access.",
		"No single food or supplement can replace comprehensive treatment for serious medical illness.",
	],
	"obesity": [
		"Obesity is a chronic, multifactorial disease associated with increased risk of diabetes, cardiovascular disease, fatty liver disease, and some cancers.",
		"Effective management usually combines nutrition counseling, physical activity support, sleep optimization, and behavior change strategies.",
		"Long-term follow-up improves outcomes because weight regulation is influenced by biological and environmental pressures.",
		"For selected patients, anti-obesity medication or bariatric surgery may be appropriate alongside lifestyle treatment.",
		"Goals should prioritize metabolic health, mobility, and quality of life rather than short-term rapid weight loss.",
		"Weight stigma can harm mental and physical health and should be actively avoided in clinical communication.",
	],
	"supplements": [
		"Supplements may be useful in specific deficiencies, but routine use without indication is not always beneficial.",
		"Product quality and ingredient concentration can vary, especially where regulation differs from prescription medicines.",
		"High doses of fat-soluble vitamins can cause toxicity affecting liver, bone, or neurological function.",
		"Herbal products and minerals may interact with anticoagulants, heart medicines, and other common prescriptions.",
		"Clinical decisions should be guided by laboratory data, symptoms, and evidence from well-designed studies.",
		"Patients should discuss all non-prescription products with clinicians to reduce avoidable harm.",
	],
	"infectious diseases": [
		"Infectious diseases are caused by microorganisms including viruses, bacteria, parasites, and fungi.",
		"Prevention measures include vaccination, hand hygiene, safer food and water, respiratory etiquette, and vector control where relevant.",
		"Early diagnosis allows timely treatment and helps limit onward transmission in households and communities.",
		"Antibiotics should be used only for bacterial infections where clinically indicated to reduce antimicrobial resistance.",
		"Infection-control practices in healthcare settings protect patients, caregivers, and health workers.",
		"Public health surveillance and transparent reporting are essential during outbreaks.",
	],
	"pregnancy": [
		"Pregnancy care includes regular antenatal visits to monitor maternal health, fetal growth, and emerging complications.",
		"Key interventions include blood pressure checks, anemia screening, gestational diabetes screening, and vaccination according to guidelines.",
		"Folic acid and balanced nutrition support fetal neural development and maternal wellbeing.",
		"Warning symptoms such as severe headache, bleeding, reduced fetal movement, or persistent abdominal pain require urgent assessment.",
		"Medication safety during pregnancy should always be reviewed with qualified professionals.",
		"Skilled birth attendance and postnatal follow-up improve outcomes for both mother and baby.",
	],
	"child health": [
		"Child health services focus on growth monitoring, developmental milestones, nutrition, immunization, and early illness recognition.",
		"Timely vaccination protects children from preventable diseases and reduces severe complications.",
		"Breastfeeding support, safe complementary feeding, and micronutrient adequacy are central to early child health.",
		"Persistent fever, breathing difficulty, dehydration, poor feeding, or lethargy should trigger prompt medical review.",
		"Developmental screening helps identify language, motor, or social concerns early, enabling targeted support.",
		"Family education on hygiene, injury prevention, and sleep routines improves long-term wellbeing.",
	],
}


STYLE_TEMPLATES = {
	"intro": [
		"Current guidance on {topic} emphasizes {focus} as a practical way to improve outcomes across diverse populations.",
		"Evidence from major public-health organizations describes {topic} as a priority area where {focus} can meaningfully reduce harm.",
		"Clinicians managing {topic} generally rely on standardized recommendations, with {focus} forming a central part of care.",
	],
	"clinical": [
		"Accurate diagnosis and risk stratification are important because treatment intensity should match clinical severity and coexisting conditions.",
		"Care plans are most effective when they combine medical therapy, structured follow-up, and patient education tailored to health literacy.",
		"Shared decision-making helps patients understand benefits, side effects, and the expected timeline for measurable improvement.",
	],
	"safety": [
		"Self-treatment based on online claims can delay proven care, so persistent or worsening symptoms should be reviewed by qualified professionals.",
		"Medication adherence and regular follow-up are essential because many complications develop gradually before obvious warning signs appear.",
		"Public messaging should prioritize verified evidence, since misinformation can reduce uptake of life-saving prevention and treatment measures.",
	],
	"prevention": [
		"At the population level, prevention is strongest when individual behavior change is supported by accessible healthcare and community services.",
		"Primary prevention, early detection, and continuity of care together provide better long-term outcomes than isolated short-term interventions.",
		"Routine checkups create opportunities to identify risk early and adjust care before irreversible complications occur.",
	],
}


def normalize_text(text: str) -> str:
	return " ".join(text.split()).strip().lower()


def word_count(text: str) -> int:
	return len(text.split())


def load_existing_entries(path: Path):
	if not path.exists():
		return []
	try:
		with path.open("r", encoding="utf-8") as file:
			data = json.load(file)
		return data if isinstance(data, list) else []
	except (json.JSONDecodeError, OSError):
		return []


def build_paragraph(topic: str, focus: str, rng: random.Random) -> str:
	sentences = [rng.choice(STYLE_TEMPLATES["intro"]).format(topic=topic, focus=focus)]

	core_facts = rng.sample(TOPIC_FACTS[topic], k=5)
	sentences.extend(core_facts)
	sentences.append(rng.choice(STYLE_TEMPLATES["clinical"]))
	sentences.append(rng.choice(STYLE_TEMPLATES["prevention"]))
	sentences.append(rng.choice(STYLE_TEMPLATES["safety"]))

	if rng.random() < 0.6:
		extra_fact = rng.choice([fact for fact in TOPIC_FACTS[topic] if fact not in core_facts])
		sentences.append(extra_fact)

	safety_expansions = STYLE_TEMPLATES["clinical"] + STYLE_TEMPLATES["prevention"] + STYLE_TEMPLATES["safety"]
	content = " ".join(sentences)

	while word_count(content) < MIN_WORDS:
		content = f"{content} {rng.choice(safety_expansions)}"

	if word_count(content) > MAX_WORDS:
		trimmed = []
		for sentence in content.split(". "):
			sentence = sentence.strip()
			if not sentence:
				continue
			if not sentence.endswith("."):
				sentence = f"{sentence}."
			candidate = " ".join(trimmed + [sentence])
			if word_count(candidate) > MAX_WORDS:
				break
			trimmed.append(sentence)
		content = " ".join(trimmed)

	if word_count(content) < MIN_WORDS:
		fallback_sentences = [
			rng.choice(TOPIC_FACTS[topic]),
			rng.choice(STYLE_TEMPLATES["prevention"]),
			rng.choice(STYLE_TEMPLATES["safety"]),
		]
		content = f"{content} {' '.join(fallback_sentences)}"

	return content


def generate_entries(existing_entries):
	target_count = random.randint(MIN_NEW_ENTRIES, MAX_NEW_ENTRIES)

	existing_signatures = {
		(entry.get("topic", ""), entry.get("source", ""), normalize_text(entry.get("content", "")))
		for entry in existing_entries
		if isinstance(entry, dict)
	}

	new_entries = []
	seen_in_run = set()

	topics = list(TOPIC_FOCUSES.keys())
	max_attempts = target_count * 40
	attempts = 0

	while len(new_entries) < target_count and attempts < max_attempts:
		attempts += 1

		topic = random.choice(topics)
		source, url = random.choice(SOURCES[topic])
		focus = random.choice(TOPIC_FOCUSES[topic])

		entry_rng = random.Random(uuid.uuid4().int)
		content = build_paragraph(topic, focus, entry_rng)
		words = word_count(content)

		if not (MIN_WORDS <= words <= MAX_WORDS):
			continue

		signature = (topic, source, normalize_text(content))
		if signature in existing_signatures or signature in seen_in_run:
			continue

		new_entries.append(
			{
				"topic": topic,
				"source": source,
				"url": url,
				"content": content,
			}
		)
		seen_in_run.add(signature)

	if len(new_entries) < target_count:
		raise RuntimeError(
			f"Could not generate enough unique entries. Generated {len(new_entries)} out of {target_count}."
		)

	return new_entries


def save_entries(path: Path, entries):
	with path.open("w", encoding="utf-8") as file:
		json.dump(entries, file, indent=2, ensure_ascii=False)


def main():
	existing_entries = load_existing_entries(OUTPUT_PATH)
	new_entries = generate_entries(existing_entries)
	combined = existing_entries + new_entries
	save_entries(OUTPUT_PATH, combined)

	print(f"Existing entries: {len(existing_entries)}")
	print(f"Newly generated entries: {len(new_entries)}")
	print(f"Total entries saved: {len(combined)}")
	print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
	main()
