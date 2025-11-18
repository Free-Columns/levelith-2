/**
 * Mock Data Generator for Admin Dashboard
 *
 * Provides realistic sample data for users, experiences, and NAICS codes
 * for testing and development purposes.
 */

// NAICS Codes Dataset (from backend/data/naics_codes_2022.json)
export const naicsCodes = [
  {
    code: "123456",
    title: "GENERAL",
    description: "General fallback classification for unspecified industries",
    industry: "general",
  },
  {
    code: "541511",
    title: "Custom Computer Programming Services",
    description:
      "Writing, modifying, testing, and supporting software to meet the needs of a particular customer",
    industry: "technology",
  },
  {
    code: "541512",
    title: "Computer Systems Design Services",
    description:
      "Planning and designing computer systems that integrate hardware, software, and communication technologies",
    industry: "technology",
  },
  {
    code: "541513",
    title: "Computer Facilities Management Services",
    description:
      "Providing on-site management and operation of clients' computer systems and/or data processing facilities",
    industry: "technology",
  },
  {
    code: "541519",
    title: "Other Computer Related Services",
    description:
      "Computer related services not elsewhere classified, such as computer disaster recovery services",
    industry: "technology",
  },
  {
    code: "541611",
    title: "Administrative Management and General Management Consulting Services",
    description:
      "Providing operating advice and assistance to businesses and other organizations",
    industry: "services",
  },
  {
    code: "541618",
    title: "Other Management Consulting Services",
    description:
      "Providing management consulting services (except administrative and general management consulting)",
    industry: "services",
  },
  {
    code: "611310",
    title: "Colleges, Universities, and Professional Schools",
    description:
      "Furnishing academic courses and granting degrees at baccalaureate or graduate levels",
    industry: "education",
  },
  {
    code: "611420",
    title: "Computer Training",
    description:
      "Offering computer and software training, including information technology (IT) training",
    industry: "education",
  },
  {
    code: "611430",
    title: "Professional and Management Development Training",
    description:
      "Offering professional development and management training courses",
    industry: "education",
  },
  {
    code: "611710",
    title: "Educational Support Services",
    description:
      "Providing non-instructional services that support educational processes or systems",
    industry: "education",
  },
  {
    code: "621111",
    title: "Offices of Physicians",
    description: "Establishments of health practitioners having the degree of M.D.",
    industry: "healthcare",
  },
  {
    code: "621511",
    title: "Medical Laboratories",
    description: "Providing analytic or diagnostic services to the medical profession",
    industry: "healthcare",
  },
  {
    code: "522110",
    title: "Commercial Banking",
    description: "Accepting deposits and making commercial, industrial, and consumer loans",
    industry: "finance",
  },
  {
    code: "522298",
    title: "All Other Nondepository Credit Intermediation",
    description: "Nondepository credit intermediation not elsewhere classified",
    industry: "finance",
  },
  {
    code: "445110",
    title: "Supermarkets and Other Grocery Stores",
    description: "Retailing a general line of food products",
    industry: "retail",
  },
  {
    code: "722511",
    title: "Full-Service Restaurants",
    description:
      "Providing food services to patrons who order and are served while seated",
    industry: "services",
  },
  {
    code: "336111",
    title: "Automobile Manufacturing",
    description: "Manufacturing complete automobiles",
    industry: "manufacturing",
  },
];

// Mock Users Generator
const firstNames = [
  "John",
  "Jane",
  "Michael",
  "Sarah",
  "David",
  "Emily",
  "Robert",
  "Jessica",
  "William",
  "Ashley",
  "James",
  "Amanda",
  "Christopher",
  "Melissa",
  "Daniel",
  "Jennifer",
  "Matthew",
  "Stephanie",
  "Andrew",
  "Nicole",
];
const lastNames = [
  "Smith",
  "Johnson",
  "Williams",
  "Brown",
  "Jones",
  "Garcia",
  "Miller",
  "Davis",
  "Rodriguez",
  "Martinez",
  "Hernandez",
  "Lopez",
  "Gonzalez",
  "Wilson",
  "Anderson",
  "Thomas",
  "Taylor",
  "Moore",
  "Jackson",
  "Martin",
];

const locations = [
  "New York, NY",
  "Los Angeles, CA",
  "Chicago, IL",
  "Houston, TX",
  "Phoenix, AZ",
  "Philadelphia, PA",
  "San Antonio, TX",
  "San Diego, CA",
  "Dallas, TX",
  "San Jose, CA",
  "Austin, TX",
  "Seattle, WA",
  "Denver, CO",
  "Boston, MA",
  "Miami, FL",
];

const bios = [
  "Software engineer passionate about building scalable applications",
  "Full-stack developer with expertise in modern web technologies",
  "Data scientist specializing in machine learning and AI",
  "UX designer focused on creating intuitive user experiences",
  "Product manager with a track record of successful launches",
  "DevOps engineer automating infrastructure at scale",
  "Mobile developer building iOS and Android applications",
  "Technical writer creating clear documentation",
  "Quality assurance engineer ensuring software reliability",
  "Database administrator optimizing performance",
];

export const generateMockUsers = (count = 20) => {
  const users = [];
  for (let i = 0; i < count; i++) {
    const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
    const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
    const username = `${firstName.toLowerCase()}${lastName.toLowerCase()}${i}`;
    const email = `${firstName.toLowerCase()}.${lastName.toLowerCase()}${i}@example.com`;

    users.push({
      id: `user_${Math.random().toString(36).substr(2, 9)}`,
      username,
      email,
      password_hash: "hashed_password_placeholder",
      is_active: Math.random() > 0.1,
      is_verified: Math.random() > 0.3,
      profile_data: {
        display_name: `${firstName} ${lastName}`,
        bio: bios[Math.floor(Math.random() * bios.length)],
        location: locations[Math.floor(Math.random() * locations.length)],
        website: Math.random() > 0.5 ? `https://${username}.dev` : null,
        avatar_url: `https://ui-avatars.com/api/?name=${firstName}+${lastName}&background=random`,
      },
      experiences: [],
      created_at: new Date(
        Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000
      ).toISOString(),
      updated_at: new Date(
        Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000
      ).toISOString(),
      last_login: new Date(
        Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000
      ).toISOString(),
    });
  }
  return users;
};

// Mock Experiences Generator
const certTitles = [
  "AWS Certified Solutions Architect",
  "Google Cloud Professional",
  "Certified Scrum Master",
  "PMP Certification",
  "Certified Kubernetes Administrator",
];

const degreeTitles = [
  "Bachelor of Science in Computer Science",
  "Master of Business Administration",
  "Bachelor of Arts in Design",
  "Master of Science in Data Science",
  "Bachelor of Engineering",
];

const courseTitles = [
  "Advanced React Development",
  "Machine Learning Fundamentals",
  "Product Management Essentials",
  "UI/UX Design Bootcamp",
  "Cloud Architecture Workshop",
];

const jobTitles = [
  "Senior Software Engineer",
  "Product Manager",
  "UX Designer",
  "Data Scientist",
  "DevOps Engineer",
  "Frontend Developer",
  "Backend Developer",
  "Mobile Developer",
  "QA Engineer",
  "Technical Writer",
];

const companies = [
  "Tech Corp",
  "Innovation Labs",
  "Digital Solutions Inc",
  "Cloud Systems",
  "Data Dynamics",
  "WebDev Pro",
  "Mobile First",
  "AI Ventures",
  "Startup Hub",
  "Enterprise Systems",
];

const skills = [
  "Python",
  "JavaScript",
  "React",
  "Node.js",
  "AWS",
  "Docker",
  "Kubernetes",
  "SQL",
  "MongoDB",
  "Git",
  "CI/CD",
  "Agile",
  "Scrum",
  "Leadership",
  "Communication",
  "Problem Solving",
];

export const generateMockExperiences = (userId, count = 5) => {
  const experiences = [];
  const types = [
    "certificate",
    "degree",
    "course",
    "gig",
    "part_time",
    "full_time",
    "soft_skill",
    "hard_skill",
    "native_skill",
  ];

  for (let i = 0; i < count; i++) {
    const type = types[Math.floor(Math.random() * types.length)];
    let category, title, description;

    // Determine category and generate appropriate data
    if (["certificate", "degree", "course"].includes(type)) {
      category = "education";
      if (type === "certificate") {
        title = certTitles[Math.floor(Math.random() * certTitles.length)];
        description = "Professional certification in specialized field";
      } else if (type === "degree") {
        title = degreeTitles[Math.floor(Math.random() * degreeTitles.length)];
        description = "Academic degree program";
      } else {
        title = courseTitles[Math.floor(Math.random() * courseTitles.length)];
        description = "Professional development course";
      }
    } else if (["gig", "part_time", "full_time"].includes(type)) {
      category = "workplace";
      title = jobTitles[Math.floor(Math.random() * jobTitles.length)];
      description = `${type.replace("_", "-")} position in technology sector`;
    } else {
      category = "skills";
      const skillName = skills[Math.floor(Math.random() * skills.length)];
      title = skillName;
      description = `Proficiency in ${skillName}`;
    }

    const startDate = new Date(
      Date.now() - Math.random() * 1095 * 24 * 60 * 60 * 1000
    );
    const isOngoing = Math.random() > 0.6;
    const endDate = isOngoing
      ? null
      : new Date(startDate.getTime() + Math.random() * 730 * 24 * 60 * 60 * 1000);

    experiences.push({
      id: `exp_${Math.random().toString(36).substr(2, 9)}`,
      user_id: userId,
      category,
      experience_type: type,
      title,
      description,
      naics_code: naicsCodes[Math.floor(Math.random() * naicsCodes.length)].code,
      start_date: startDate.toISOString(),
      end_date: endDate ? endDate.toISOString() : null,
      organization:
        category === "workplace"
          ? companies[Math.floor(Math.random() * companies.length)]
          : category === "education"
          ? "University of Technology"
          : null,
      location:
        category !== "skills"
          ? locations[Math.floor(Math.random() * locations.length)]
          : null,
      skills_gained: Array.from(
        { length: Math.floor(Math.random() * 5) + 1 },
        () => skills[Math.floor(Math.random() * skills.length)]
      ),
      achievements:
        category === "workplace"
          ? ["Led team of 5 developers", "Increased performance by 40%"]
          : [],
      metadata: {},
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  }

  return experiences;
};

// Generate initial dataset
export const mockUsers = generateMockUsers(25);

// Add experiences to users
mockUsers.forEach((user) => {
  const userExperiences = generateMockExperiences(
    user.id,
    Math.floor(Math.random() * 8) + 2
  );
  user.experiences = userExperiences.map((exp) => exp.id);
});

// Flatten all experiences
export const mockExperiences = mockUsers.flatMap((user) =>
  generateMockExperiences(user.id, Math.floor(Math.random() * 8) + 2)
);

// Statistics Helper
export const getStatistics = () => {
  const totalUsers = mockUsers.length;
  const activeUsers = mockUsers.filter((u) => u.is_active).length;
  const verifiedUsers = mockUsers.filter((u) => u.is_verified).length;
  const totalExperiences = mockExperiences.length;

  const experiencesByType = mockExperiences.reduce((acc, exp) => {
    acc[exp.experience_type] = (acc[exp.experience_type] || 0) + 1;
    return acc;
  }, {});

  const experiencesByCategory = mockExperiences.reduce((acc, exp) => {
    acc[exp.category] = (acc[exp.category] || 0) + 1;
    return acc;
  }, {});

  const experiencesByNAICS = mockExperiences.reduce((acc, exp) => {
    const naics = naicsCodes.find((n) => n.code === exp.naics_code);
    if (naics) {
      const industry = naics.industry;
      acc[industry] = (acc[industry] || 0) + 1;
    }
    return acc;
  }, {});

  return {
    users: {
      total: totalUsers,
      active: activeUsers,
      verified: verifiedUsers,
      inactive: totalUsers - activeUsers,
    },
    experiences: {
      total: totalExperiences,
      byType: experiencesByType,
      byCategory: experiencesByCategory,
      byIndustry: experiencesByNAICS,
    },
  };
};

export default {
  naicsCodes,
  mockUsers,
  mockExperiences,
  generateMockUsers,
  generateMockExperiences,
  getStatistics,
};
