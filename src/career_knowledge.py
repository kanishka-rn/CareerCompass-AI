"""Canonical career knowledge used by the CareerCompass hybrid engine."""
from skill_normalizer import normalize_skills

_DATA = {
"Software Development":
 ("Software Developer,Backend Developer,Frontend Developer,Full Stack Developer,Mobile Developer", "python,java,javascript,data structures and algorithms,algorithms,git,sql,html,css", "programming,coding,software development,web development,app development", "Build programming fundamentals|Practice data structures and algorithms|Build and test applications|Use Git for collaborative development|Create a portfolio|Prepare for interviews"),
"AI & Machine Learning": 
("Machine Learning Engineer,AI Engineer,Data Scientist,NLP Engineer,Computer Vision Engineer", "python,machine learning,statistics,numpy,pandas,scikit-learn,deep learning,tensorflow,pytorch", "artificial intelligence,machine learning,data science,deep learning,natural language processing,computer vision", "Strengthen Python for data work|Learn NumPy and Pandas|Study statistics and machine learning|Build ML projects|Explore deep learning|Deploy an end-to-end model"),
"Data & Analytics": 
("Data Analyst,Business Intelligence Analyst,Data Engineer,Analytics Engineer", "python,sql,statistics,excel,power bi,tableau,pandas,numpy,data analysis", "data analysis,data science,analytics,business intelligence,visualization", "Learn spreadsheet and data fundamentals|Master SQL queries|Use Python for analysis|Study statistics|Build dashboards|Publish portfolio case studies"),
"Cloud & DevOps": 
("Cloud Engineer,DevOps Engineer,Site Reliability Engineer,Platform Engineer", "linux,networking,aws,docker,kubernetes,git,ci/cd,python", "cloud computing,devops,automation,infrastructure,servers", "Learn Linux and networking|Practice Git and scripting|Deploy a cloud service|Containerize applications with Docker|Learn CI/CD|Operate a Kubernetes project"),
"Cybersecurity": 
("Cybersecurity Analyst,Security Engineer,Penetration Tester,SOC Analyst", "linux,networking,python,cybersecurity,ethical hacking,burp suite,wireshark,cryptography", "cybersecurity,ethical hacking,security,penetration testing,network security", "Learn networking and Linux|Understand security fundamentals|Practice in legal labs|Learn web security tools|Document security projects|Prepare for certifications"),
"Mechanical Engineering": 
("Mechanical Engineer,Design Engineer,Manufacturing Engineer,Robotics Engineer", "cad,solidworks,autocad,thermodynamics,manufacturing,robotics", "mechanical engineering,machines,robotics,automobiles,manufacturing", "Strengthen engineering fundamentals|Develop CAD proficiency|Study materials and thermodynamics|Complete a design project|Learn manufacturing processes|Build an engineering portfolio"),
"Civil Engineering": 
("Civil Engineer,Structural Engineer,Construction Engineer,Site Engineer", "autocad,structural analysis,construction,surveying,project management", "civil engineering,construction,buildings,infrastructure,structural design", "Strengthen civil fundamentals|Learn CAD and surveying|Study structural analysis|Explore construction planning|Complete a design case study|Gain site experience"),
"Electronics Engineering": 
("Electronics Engineer,Embedded Systems Engineer,VLSI Engineer,IoT Engineer", "electronics,embedded systems,microcontrollers,iot,pcb design,vlsi,arduino,c programming", "electronics,embedded systems,iot,hardware,microcontrollers,vlsi", "Master circuit fundamentals|Program microcontrollers|Build embedded projects|Learn PCB design|Explore IoT or VLSI|Create a hardware portfolio"),
"Electrical Engineering": 
("Electrical Engineer,Power Systems Engineer,Control Systems Engineer,Automation Engineer", "electrical engineering,power systems,circuits,control systems,automation,matlab", "electrical engineering,electricity,power systems,automation,renewable energy", "Strengthen circuits and systems|Study power systems|Learn control fundamentals|Use simulation tools|Build an automation project|Explore renewable energy"),
"Finance & Accounting": 
("Financial Analyst,Accountant,Investment Analyst,Auditor", "accounting,finance,excel,financial analysis,financial modeling,taxation,auditing", "finance,accounting,investment,banking,financial analysis", "Learn accounting fundamentals|Master Excel|Study financial statements|Practice financial analysis|Build modeling projects|Seek internships or credentials"),
"Business & Management":
 ("Business Analyst,Project Manager,Operations Manager,Product Manager", "communication,leadership,project management,business analysis,management,excel", "business,management,leadership,entrepreneurship,strategy,product management", "Develop business fundamentals|Improve communication|Learn project planning|Practice business analysis|Lead a project|Build professional experience"),
"Marketing": 
("Digital Marketing Specialist,SEO Specialist,Content Strategist,Brand Manager", "marketing,digital marketing,seo,content marketing,social media marketing,analytics", "marketing,branding,advertising,social media,digital marketing,content creation", "Learn marketing foundations|Study audience research|Practice SEO and content|Run a small campaign|Measure analytics|Build a campaign portfolio"),
"Medicine": 
("Doctor,Medical Researcher,Clinical Specialist,Physician", "biology,anatomy,physiology,medicine,clinical skills,diagnosis", "medicine,health,medical science,patient care,biology", "Strengthen medical science|Develop clinical knowledge|Practice patient communication|Explore specialties|Gain supervised clinical experience|Continue professional training"),
"Pharmacy": 
("Pharmacist,Clinical Pharmacist,Pharmaceutical Researcher,Drug Safety Specialist", "pharmacy,pharmacology,chemistry,drug development,clinical research", "pharmacy,medicine,drugs,pharmaceutical research,healthcare", "Master pharmacology|Study pharmaceutical chemistry|Learn regulations|Explore clinical pharmacy|Develop research literacy|Gain clinical or industry experience"),
"Healthcare": 
("Healthcare Administrator,Public Health Specialist,Clinical Coordinator,Healthcare Analyst", "healthcare,patient care,public health,health management,clinical research,biology", "healthcare,public health,patient care,health management,medical services", "Learn healthcare systems|Strengthen patient communication|Study public health|Explore healthcare management|Practice data-informed care|Gain field experience"),
"Scientific Research": 
("Research Scientist,Research Associate,Laboratory Scientist,Academic Researcher", "research,statistics,data analysis,mathematics,python,scientific method", "research,science,experiments,discovery,scientific research", "Strengthen subject fundamentals|Learn research methodology|Study statistics|Read research papers critically|Conduct a supervised project|Present findings"),
"UI/UX & Design":
 ("UI Designer,UX Designer,Product Designer,UX Researcher", "ui,ux,figma,prototyping,user research,design,wireframing", "ui design,ux design,user experience,visual design,product design,creative design", "Learn design principles|Master Figma|Practice user research|Create wireframes and prototypes|Build case studies|Publish a portfolio"),
}
CAREER_ROLES = {domain: roles.split(",") for domain, (roles, _, _, _) in _DATA.items()}
CAREER_SKILLS = {domain: normalize_skills(skills) for domain, (_, skills, _, _) in _DATA.items()}
CAREER_INTERESTS = {domain: interests.split(",") for domain, (_, _, interests, _) in _DATA.items()}
CAREER_ROADMAPS = {domain: roadmap.split("|") for domain, (_, _, _, roadmap) in _DATA.items()}
DOMAIN_KEYWORDS = {domain: set(CAREER_SKILLS[domain] + CAREER_INTERESTS[domain]) for domain in _DATA}

