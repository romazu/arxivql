import dataclasses


@dataclasses.dataclass
class Category:
    id: str
    name: str
    group_name: str
    archive_id: str
    archive_name: str
    description: str

    def __str__(self):
        return self.to_string()

    def to_string(self):
        return self.id


# StringableMeta is used as metaclass factory to add
# noinspection PyPep8Naming
# noinspection SpellCheckingInspection
def StringableMeta(s: str):
    class _StringableMeta(type):
        def __str__(cls):
            return s

        @staticmethod
        def to_string():
            return s

    return _StringableMeta


@dataclasses.dataclass
class Taxonomy:
    """
    https://arxiv.org/category_taxonomy
    """

    @dataclasses.dataclass
    class cs(metaclass=StringableMeta("cs.*")):
        AI = Category(
            id="cs.AI",
            name="Artificial Intelligence",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers all areas of AI except Vision, Robotics, Machine Learning, Multiagent Systems, and Computation and Language (Natural Language Processing), which have separate subject areas. In particular, includes Expert Systems, Theorem Proving (although this may overlap with Logic in Computer Science), Knowledge Representation, Planning, and Uncertainty in AI. Roughly includes material in ACM Subject Classes I.2.0, I.2.1, I.2.3, I.2.4, I.2.8, and I.2.11.",
        )
        AR = Category(
            id="cs.AR",
            name="Hardware Architecture",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers systems organization and hardware architecture. Roughly includes material in ACM Subject Classes C.0, C.1, and C.5.",
        )
        CC = Category(
            id="cs.CC",
            name="Computational Complexity",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers models of computation, complexity classes, structural complexity, complexity tradeoffs, upper and lower bounds. Roughly includes material in ACM Subject Classes F.1 (computation by abstract devices), F.2.3 (tradeoffs among complexity measures), and F.4.3 (formal languages), although some material in formal languages may be more appropriate for Logic in Computer Science. Some material in F.2.1 and F.2.2, may also be appropriate here, but is more likely to have Data Structures and Algorithms as the primary subject area.",
        )
        CE = Category(
            id="cs.CE",
            name="Computational Engineering, Finance, and Science",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers applications of computer science to the mathematical modeling of complex systems in the fields of science, engineering, and finance. Papers here are interdisciplinary and applications-oriented, focusing on techniques and tools that enable challenging computational simulations to be performed, for which the use of supercomputers or distributed computing platforms is often required. Includes material in ACM Subject Classes J.2, J.3, and J.4 (economics).",
        )
        CG = Category(
            id="cs.CG",
            name="Computational Geometry",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Roughly includes material in ACM Subject Classes I.3.5 and F.2.2.",
        )
        CL = Category(
            id="cs.CL",
            name="Computation and Language",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers natural language processing. Roughly includes material in ACM Subject Class I.2.7. Note that work on artificial languages (programming languages, logics, formal systems) that does not explicitly address natural-language issues broadly construed (natural-language processing, computational linguistics, speech, text retrieval, etc.) is not appropriate for this area.",
        )
        CR = Category(
            id="cs.CR",
            name="Cryptography and Security",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers all areas of cryptography and security including authentication, public key cryptosytems, proof-carrying code, etc. Roughly includes material in ACM Subject Classes D.4.6 and E.3.",
        )
        CV = Category(
            id="cs.CV",
            name="Computer Vision and Pattern Recognition",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers image processing, computer vision, pattern recognition, and scene understanding. Roughly includes material in ACM Subject Classes I.2.10, I.4, and I.5.",
        )
        CY = Category(
            id="cs.CY",
            name="Computers and Society",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers impact of computers on society, computer ethics, information technology and public policy, legal aspects of computing, computers and education. Roughly includes material in ACM Subject Classes K.0, K.2, K.3, K.4, K.5, and K.7.",
        )
        DB = Category(
            id="cs.DB",
            name="Databases",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers database management, datamining, and data processing. Roughly includes material in ACM Subject Classes E.2, E.5, H.0, H.2, and J.1.",
        )
        DC = Category(
            id="cs.DC",
            name="Distributed, Parallel, and Cluster Computing",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers fault-tolerance, distributed algorithms, stabilility, parallel computation, and cluster computing. Roughly includes material in ACM Subject Classes C.1.2, C.1.4, C.2.4, D.1.3, D.4.5, D.4.7, E.1.",
        )
        DL = Category(
            id="cs.DL",
            name="Digital Libraries",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers all aspects of the digital library design and document and text creation. Note that there will be some overlap with Information Retrieval (which is a separate subject area). Roughly includes material in ACM Subject Classes H.3.5, H.3.6, H.3.7, I.7.",
        )
        DM = Category(
            id="cs.DM",
            name="Discrete Mathematics",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers combinatorics, graph theory, applications of probability. Roughly includes material in ACM Subject Classes G.2 and G.3.",
        )
        DS = Category(
            id="cs.DS",
            name="Data Structures and Algorithms",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers data structures and analysis of algorithms. Roughly includes material in ACM Subject Classes E.1, E.2, F.2.1, and F.2.2.",
        )
        ET = Category(
            id="cs.ET",
            name="Emerging Technologies",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers approaches to information processing (computing, communication, sensing) and bio-chemical analysis based on alternatives to silicon CMOS-based technologies, such as nanoscale electronic, photonic, spin-based, superconducting, mechanical, bio-chemical and quantum technologies (this list is not exclusive). Topics of interest include (1) building blocks for emerging technologies, their scalability and adoption in larger systems, including integration with traditional technologies, (2) modeling, design and optimization of novel devices and systems, (3) models of computation, algorithm design and programming for emerging technologies.",
        )
        FL = Category(
            id="cs.FL",
            name="Formal Languages and Automata Theory",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers automata theory, formal language theory, grammars, and combinatorics on words. This roughly corresponds to ACM Subject Classes F.1.1, and F.4.3. Papers dealing with computational complexity should go to cs.CC; papers dealing with logic should go to cs.LO.",
        )
        GL = Category(
            id="cs.GL",
            name="General Literature",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers introductory material, survey material, predictions of future trends, biographies, and miscellaneous computer-science related material. Roughly includes all of ACM Subject Class A, except it does not include conference proceedings (which will be listed in the appropriate subject area).",
        )
        GR = Category(
            id="cs.GR",
            name="Graphics",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers all aspects of computer graphics. Roughly includes material in all of ACM Subject Class I.3, except that I.3.5 is is likely to have Computational Geometry as the primary subject area.",
        )
        GT = Category(
            id="cs.GT",
            name="Computer Science and Game Theory",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers all theoretical and applied aspects at the intersection of computer science and game theory, including work in mechanism design, learning in games (which may overlap with Learning), foundations of agent modeling in games (which may overlap with Multiagent systems), coordination, specification and formal methods for non-cooperative computational environments. The area also deals with applications of game theory to areas such as electronic commerce.",
        )
        HC = Category(
            id="cs.HC",
            name="Human-Computer Interaction",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers human factors, user interfaces, and collaborative computing. Roughly includes material in ACM Subject Classes H.1.2 and all of H.5, except for H.5.1, which is more likely to have Multimedia as the primary subject area.",
        )
        IR = Category(
            id="cs.IR",
            name="Information Retrieval",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers indexing, dictionaries, retrieval, content and analysis. Roughly includes material in ACM Subject Classes H.3.0, H.3.1, H.3.2, H.3.3, and H.3.4.",
        )
        IT = Category(
            id="cs.IT",
            name="Information Theory",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers theoretical and experimental aspects of information theory and coding. Includes material in ACM Subject Class E.4 and intersects with H.1.1.",
        )
        LG = Category(
            id="cs.LG",
            name="Machine Learning",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Papers on all aspects of machine learning research (supervised, unsupervised, reinforcement learning, bandit problems, and so on) including also robustness, explanation, fairness, and methodology. cs.LG is also an appropriate primary category for applications of machine learning methods.",
        )
        LO = Category(
            id="cs.LO",
            name="Logic in Computer Science",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers all aspects of logic in computer science, including finite model theory, logics of programs, modal logic, and program verification. Programming language semantics should have Programming Languages as the primary subject area. Roughly includes material in ACM Subject Classes D.2.4, F.3.1, F.4.0, F.4.1, and F.4.2; some material in F.4.3 (formal languages) may also be appropriate here, although Computational Complexity is typically the more appropriate subject area.",
        )
        MA = Category(
            id="cs.MA",
            name="Multiagent Systems",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers multiagent systems, distributed artificial intelligence, intelligent agents, coordinated interactions. and practical applications. Roughly covers ACM Subject Class I.2.11.",
        )
        MM = Category(
            id="cs.MM",
            name="Multimedia",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Roughly includes material in ACM Subject Class H.5.1.",
        )
        MS = Category(
            id="cs.MS",
            name="Mathematical Software",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Roughly includes material in ACM Subject Class G.4.",
        )
        NA = Category(
            id="cs.NA",
            name="Numerical Analysis",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="cs.NA is an alias for math.NA. Roughly includes material in ACM Subject Class G.1.",
        )
        NE = Category(
            id="cs.NE",
            name="Neural and Evolutionary Computing",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers neural networks, connectionism, genetic algorithms, artificial life, adaptive behavior. Roughly includes some material in ACM Subject Class C.1.3, I.2.6, I.5.",
        )
        NI = Category(
            id="cs.NI",
            name="Networking and Internet Architecture",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers all aspects of computer communication networks, including network architecture and design, network protocols, and internetwork standards (like TCP/IP). Also includes topics, such as web caching, that are directly relevant to Internet architecture and performance. Roughly includes all of ACM Subject Class C.2 except C.2.4, which is more likely to have Distributed, Parallel, and Cluster Computing as the primary subject area.",
        )
        OH = Category(
            id="cs.OH",
            name="Other Computer Science",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="This is the classification to use for documents that do not fit anywhere else.",
        )
        OS = Category(
            id="cs.OS",
            name="Operating Systems",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Roughly includes material in ACM Subject Classes D.4.1, D.4.2., D.4.3, D.4.4, D.4.5, D.4.7, and D.4.9.",
        )
        PF = Category(
            id="cs.PF",
            name="Performance",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers performance measurement and evaluation, queueing, and simulation. Roughly includes material in ACM Subject Classes D.4.8 and K.6.2.",
        )
        PL = Category(
            id="cs.PL",
            name="Programming Languages",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers programming language semantics, language features, programming approaches (such as object-oriented programming, functional programming, logic programming). Also includes material on compilers oriented towards programming languages; other material on compilers may be more appropriate in Architecture (AR). Roughly includes material in ACM Subject Classes D.1 and D.3.",
        )
        RO = Category(
            id="cs.RO",
            name="Robotics",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Roughly includes material in ACM Subject Class I.2.9.",
        )
        SC = Category(
            id="cs.SC",
            name="Symbolic Computation",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Roughly includes material in ACM Subject Class I.1.",
        )
        SD = Category(
            id="cs.SD",
            name="Sound",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers all aspects of computing with sound, and sound as an information channel. Includes models of sound, analysis and synthesis, audio user interfaces, sonification of data, computer music, and sound signal processing. Includes ACM Subject Class H.5.5, and intersects with H.1.2, H.5.1, H.5.2, I.2.7, I.5.4, I.6.3, J.5, K.4.2.",
        )
        SE = Category(
            id="cs.SE",
            name="Software Engineering",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers design tools, software metrics, testing and debugging, programming environments, etc. Roughly includes material in all of ACM Subject Classes D.2, except that D.2.4 (program verification) should probably have Logics in Computer Science as the primary subject area.",
        )
        SI = Category(
            id="cs.SI",
            name="Social and Information Networks",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="Covers the design, analysis, and modeling of social and information networks, including their applications for on-line information access, communication, and interaction, and their roles as datasets in the exploration of questions in these and other domains, including connections to the social and biological sciences. Analysis and modeling of such networks includes topics in ACM Subject classes F.2, G.2, G.3, H.2, and I.2; applications in computing include topics in H.3, H.4, and H.5; and applications at the interface of computing and other disciplines include topics in J.1--J.7. Papers on computer communication systems and network protocols (e.g. TCP/IP) are generally a closer fit to the Networking and Internet Architecture (cs.NI) category.",
        )
        SY = Category(
            id="cs.SY",
            name="Systems and Control",
            group_name="Computer Science",
            archive_id="cs",
            archive_name="Computer Science",
            description="cs.SY is an alias for eess.SY. This section includes theoretical and experimental research covering all facets of automatic control systems. The section is focused on methods of control system analysis and design using tools of modeling, simulation and optimization. Specific areas of research include nonlinear, distributed, adaptive, stochastic and robust control in addition to hybrid and discrete event systems. Application areas include automotive and aerospace control systems, network control, biological systems, multiagent and cooperative control, robotics, reinforcement learning, sensor networks, control of cyber-physical and energy-related systems, and control of computing systems.",
        )

    @dataclasses.dataclass
    class econ(metaclass=StringableMeta("econ.*")):
        EM = Category(
            id="econ.EM",
            name="Econometrics",
            group_name="Economics",
            archive_id="econ",
            archive_name="Economics",
            description="Econometric Theory, Micro-Econometrics, Macro-Econometrics, Empirical Content of Economic Relations discovered via New Methods, Methodological Aspects of the Application of Statistical Inference to Economic Data.",
        )
        GN = Category(
            id="econ.GN",
            name="General Economics",
            group_name="Economics",
            archive_id="econ",
            archive_name="Economics",
            description="General methodological, applied, and empirical contributions to economics.",
        )
        TH = Category(
            id="econ.TH",
            name="Theoretical Economics",
            group_name="Economics",
            archive_id="econ",
            archive_name="Economics",
            description="Includes theoretical contributions to Contract Theory, Decision Theory, Game Theory, General Equilibrium, Growth, Learning and Evolution, Macroeconomics, Market and Mechanism Design, and Social Choice.",
        )

    @dataclasses.dataclass
    class eess(metaclass=StringableMeta("eess.*")):
        AS = Category(
            id="eess.AS",
            name="Audio and Speech Processing",
            group_name="Electrical Engineering and Systems Science",
            archive_id="eess",
            archive_name="Electrical Engineering and Systems Science",
            description="Theory and methods for processing signals representing audio, speech, and language, and their applications. This includes analysis, synthesis, enhancement, transformation, classification and interpretation of such signals as well as the design, development, and evaluation of associated signal processing systems. Machine learning and pattern analysis applied to any of the above areas is also welcome. Specific topics of interest include: auditory modeling and hearing aids; acoustic beamforming and source localization; classification of acoustic scenes; speaker separation; active noise control and echo cancellation; enhancement; de-reverberation; bioacoustics; music signals analysis, synthesis and modification; music information retrieval; audio for multimedia and joint audio-video processing; spoken and written language modeling, segmentation, tagging, parsing, understanding, and translation; text mining; speech production, perception, and psychoacoustics; speech analysis, synthesis, and perceptual modeling and coding; robust speech recognition; speaker recognition and characterization; deep learning, online learning, and graphical models applied to speech, audio, and language signals; and implementation aspects ranging from system architecture to fast algorithms.",
        )
        IV = Category(
            id="eess.IV",
            name="Image and Video Processing",
            group_name="Electrical Engineering and Systems Science",
            archive_id="eess",
            archive_name="Electrical Engineering and Systems Science",
            description="Theory, algorithms, and architectures for the formation, capture, processing, communication, analysis, and display of images, video, and multidimensional signals in a wide variety of applications. Topics of interest include: mathematical, statistical, and perceptual image and video modeling and representation; linear and nonlinear filtering, de-blurring, enhancement, restoration, and reconstruction from degraded, low-resolution or tomographic data; lossless and lossy compression and coding; segmentation, alignment, and recognition; image rendering, visualization, and printing; computational imaging, including ultrasound, tomographic and magnetic resonance imaging; and image and video analysis, synthesis, storage, search and retrieval.",
        )
        SP = Category(
            id="eess.SP",
            name="Signal Processing",
            group_name="Electrical Engineering and Systems Science",
            archive_id="eess",
            archive_name="Electrical Engineering and Systems Science",
            description='Theory, algorithms, performance analysis and applications of signal and data analysis, including physical modeling, processing, detection and parameter estimation, learning, mining, retrieval, and information extraction. The term "signal" includes speech, audio, sonar, radar, geophysical, physiological, (bio-) medical, image, video, and multimodal natural and man-made signals, including communication signals and data. Topics of interest include: statistical signal processing, spectral estimation and system identification; filter design, adaptive filtering / stochastic learning; (compressive) sampling, sensing, and transform-domain methods including fast algorithms; signal processing for machine learning and machine learning for signal processing applications; in-network and graph signal processing; convex and nonconvex optimization methods for signal processing applications; radar, sonar, and sensor array beamforming and direction finding; communications signal processing; low power, multi-core and system-on-chip signal processing; sensing, communication, analysis and optimization for cyber-physical systems such as power grids and the Internet of Things.',
        )
        SY = Category(
            id="eess.SY",
            name="Systems and Control",
            group_name="Electrical Engineering and Systems Science",
            archive_id="eess",
            archive_name="Electrical Engineering and Systems Science",
            description="This section includes theoretical and experimental research covering all facets of automatic control systems. The section is focused on methods of control system analysis and design using tools of modeling, simulation and optimization. Specific areas of research include nonlinear, distributed, adaptive, stochastic and robust control in addition to hybrid and discrete event systems. Application areas include automotive and aerospace control systems, network control, biological systems, multiagent and cooperative control, robotics, reinforcement learning, sensor networks, control of cyber-physical and energy-related systems, and control of computing systems.",
        )

    @dataclasses.dataclass
    class math(metaclass=StringableMeta("math.*")):
        AC = Category(
            id="math.AC",
            name="Commutative Algebra",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Commutative rings, modules, ideals, homological algebra, computational aspects, invariant theory, connections to algebraic geometry and combinatorics",
        )
        AG = Category(
            id="math.AG",
            name="Algebraic Geometry",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Algebraic varieties, stacks, sheaves, schemes, moduli spaces, complex geometry, quantum cohomology",
        )
        AP = Category(
            id="math.AP",
            name="Analysis of PDEs",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Existence and uniqueness, boundary conditions, linear and non-linear operators, stability, soliton theory, integrable PDE's, conservation laws, qualitative dynamics",
        )
        AT = Category(
            id="math.AT",
            name="Algebraic Topology",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Homotopy theory, homological algebra, algebraic treatments of manifolds",
        )
        CA = Category(
            id="math.CA",
            name="Classical Analysis and ODEs",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Special functions, orthogonal polynomials, harmonic analysis, ODE's, differential relations, calculus of variations, approximations, expansions, asymptotics",
        )
        CO = Category(
            id="math.CO",
            name="Combinatorics",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Discrete mathematics, graph theory, enumeration, combinatorial optimization, Ramsey theory, combinatorial game theory",
        )
        CT = Category(
            id="math.CT",
            name="Category Theory",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Enriched categories, topoi, abelian categories, monoidal categories, homological algebra",
        )
        CV = Category(
            id="math.CV",
            name="Complex Variables",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Holomorphic functions, automorphic group actions and forms, pseudoconvexity, complex geometry, analytic spaces, analytic sheaves",
        )
        DG = Category(
            id="math.DG",
            name="Differential Geometry",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Complex, contact, Riemannian, pseudo-Riemannian and Finsler geometry, relativity, gauge theory, global analysis",
        )
        DS = Category(
            id="math.DS",
            name="Dynamical Systems",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Dynamics of differential equations and flows, mechanics, classical few-body problems, iterations, complex dynamics, delayed differential equations",
        )
        FA = Category(
            id="math.FA",
            name="Functional Analysis",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Banach spaces, function spaces, real functions, integral transforms, theory of distributions, measure theory",
        )
        GM = Category(
            id="math.GM",
            name="General Mathematics",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Mathematical material of general interest, topics not covered elsewhere",
        )
        GN = Category(
            id="math.GN",
            name="General Topology",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Continuum theory, point-set topology, spaces with algebraic structure, foundations, dimension theory, local and global properties",
        )
        GR = Category(
            id="math.GR",
            name="Group Theory",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Finite groups, topological groups, representation theory, cohomology, classification and structure",
        )
        GT = Category(
            id="math.GT",
            name="Geometric Topology",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Manifolds, orbifolds, polyhedra, cell complexes, foliations, geometric structures",
        )
        HO = Category(
            id="math.HO",
            name="History and Overview",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Biographies, philosophy of mathematics, mathematics education, recreational mathematics, communication of mathematics, ethics in mathematics",
        )
        IT = Category(
            id="math.IT",
            name="Information Theory",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="math.IT is an alias for cs.IT. Covers theoretical and experimental aspects of information theory and coding.",
        )
        KT = Category(
            id="math.KT",
            name="K-Theory and Homology",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Algebraic and topological K-theory, relations with topology, commutative algebra, and operator algebras",
        )
        LO = Category(
            id="math.LO",
            name="Logic",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Logic, set theory, point-set topology, formal mathematics",
        )
        MG = Category(
            id="math.MG",
            name="Metric Geometry",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Euclidean, hyperbolic, discrete, convex, coarse geometry, comparisons in Riemannian geometry, symmetric spaces",
        )
        MP = Category(
            id="math.MP",
            name="Mathematical Physics",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="math.MP is an alias for math-ph. Articles in this category focus on areas of research that illustrate the application of mathematics to problems in physics, develop mathematical methods for such applications, or provide mathematically rigorous formulations of existing physical theories. Submissions to math-ph should be of interest to both physically oriented mathematicians and mathematically oriented physicists; submissions which are primarily of interest to theoretical physicists or to mathematicians should probably be directed to the respective physics/math categories",
        )
        NA = Category(
            id="math.NA",
            name="Numerical Analysis",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Numerical algorithms for problems in analysis and algebra, scientific computation",
        )
        NT = Category(
            id="math.NT",
            name="Number Theory",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Prime numbers, diophantine equations, analytic number theory, algebraic number theory, arithmetic geometry, Galois theory",
        )
        OA = Category(
            id="math.OA",
            name="Operator Algebras",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Algebras of operators on Hilbert space, C^*-algebras, von Neumann algebras, non-commutative geometry",
        )
        OC = Category(
            id="math.OC",
            name="Optimization and Control",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Operations research, linear programming, control theory, systems theory, optimal control, game theory",
        )
        PR = Category(
            id="math.PR",
            name="Probability",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Theory and applications of probability and stochastic processes: e.g. central limit theorems, large deviations, stochastic differential equations, models from statistical mechanics, queuing theory",
        )
        QA = Category(
            id="math.QA",
            name="Quantum Algebra",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Quantum groups, skein theories, operadic and diagrammatic algebra, quantum field theory",
        )
        RA = Category(
            id="math.RA",
            name="Rings and Algebras",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Non-commutative rings and algebras, non-associative algebras, universal algebra and lattice theory, linear algebra, semigroups",
        )
        RT = Category(
            id="math.RT",
            name="Representation Theory",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Linear representations of algebras and groups, Lie theory, associative algebras, multilinear algebra",
        )
        SG = Category(
            id="math.SG",
            name="Symplectic Geometry",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Hamiltonian systems, symplectic flows, classical integrable systems",
        )
        SP = Category(
            id="math.SP",
            name="Spectral Theory",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Schrodinger operators, operators on manifolds, general differential operators, numerical studies, integral operators, discrete models, resonances, non-self-adjoint operators, random operators/matrices",
        )
        ST = Category(
            id="math.ST",
            name="Statistics Theory",
            group_name="Mathematics",
            archive_id="math",
            archive_name="Mathematics",
            description="Applied, computational and theoretical statistics: e.g. statistical inference, regression, time series, multivariate analysis, data analysis, Markov chain Monte Carlo, design of experiments, case studies",
        )

    @dataclasses.dataclass
    class q_bio(metaclass=StringableMeta("q-bio.*")):
        BM = Category(
            id="q-bio.BM",
            name="Biomolecules",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="DNA, RNA, proteins, lipids, etc.; molecular structures and folding kinetics; molecular interactions; single-molecule manipulation.",
        )
        CB = Category(
            id="q-bio.CB",
            name="Cell Behavior",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="Cell-cell signaling and interaction; morphogenesis and development; apoptosis; bacterial conjugation; viral-host interaction; immunology",
        )
        GN = Category(
            id="q-bio.GN",
            name="Genomics",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="DNA sequencing and assembly; gene and motif finding; RNA editing and alternative splicing; genomic structure and processes (replication, transcription, methylation, etc); mutational processes.",
        )
        MN = Category(
            id="q-bio.MN",
            name="Molecular Networks",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="Gene regulation, signal transduction, proteomics, metabolomics, gene and enzymatic networks",
        )
        NC = Category(
            id="q-bio.NC",
            name="Neurons and Cognition",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="Synapse, cortex, neuronal dynamics, neural network, sensorimotor control, behavior, attention",
        )
        OT = Category(
            id="q-bio.OT",
            name="Other Quantitative Biology",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="Work in quantitative biology that does not fit into the other q-bio classifications",
        )
        PE = Category(
            id="q-bio.PE",
            name="Populations and Evolution",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="Population dynamics, spatio-temporal and epidemiological models, dynamic speciation, co-evolution, biodiversity, foodwebs, aging; molecular evolution and phylogeny; directed evolution; origin of life",
        )
        QM = Category(
            id="q-bio.QM",
            name="Quantitative Methods",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="All experimental, numerical, statistical and mathematical contributions of value to biology",
        )
        SC = Category(
            id="q-bio.SC",
            name="Subcellular Processes",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="Assembly and control of subcellular structures (channels, organelles, cytoskeletons, capsules, etc.); molecular motors, transport, subcellular localization; mitosis and meiosis",
        )
        TO = Category(
            id="q-bio.TO",
            name="Tissues and Organs",
            group_name="Quantitative Biology",
            archive_id="q-bio",
            archive_name="Quantitative Biology",
            description="Blood flow in vessels, biomechanics of bones, electrical waves, endocrine system, tumor growth",
        )

    @dataclasses.dataclass
    class q_fin(metaclass=StringableMeta("q-fin.*")):
        CP = Category(
            id="q-fin.CP",
            name="Computational Finance",
            group_name="Quantitative Finance",
            archive_id="q-fin",
            archive_name="Quantitative Finance",
            description="Computational methods, including Monte Carlo, PDE, lattice and other numerical methods with applications to financial modeling",
        )
        EC = Category(
            id="q-fin.EC",
            name="Economics",
            group_name="Quantitative Finance",
            archive_id="q-fin",
            archive_name="Quantitative Finance",
            description="q-fin.EC is an alias for econ.GN. Economics, including micro and macro economics, international economics, theory of the firm, labor economics, and other economic topics outside finance",
        )
        GN = Category(
            id="q-fin.GN",
            name="General Finance",
            group_name="Quantitative Finance",
            archive_id="q-fin",
            archive_name="Quantitative Finance",
            description="Development of general quantitative methodologies with applications in finance",
        )
        MF = Category(
            id="q-fin.MF",
            name="Mathematical Finance",
            group_name="Quantitative Finance",
            archive_id="q-fin",
            archive_name="Quantitative Finance",
            description="Mathematical and analytical methods of finance, including stochastic, probabilistic and functional analysis, algebraic, geometric and other methods",
        )
        PM = Category(
            id="q-fin.PM",
            name="Portfolio Management",
            group_name="Quantitative Finance",
            archive_id="q-fin",
            archive_name="Quantitative Finance",
            description="Security selection and optimization, capital allocation, investment strategies and performance measurement",
        )
        PR = Category(
            id="q-fin.PR",
            name="Pricing of Securities",
            group_name="Quantitative Finance",
            archive_id="q-fin",
            archive_name="Quantitative Finance",
            description="Valuation and hedging of financial securities, their derivatives, and structured products",
        )
        RM = Category(
            id="q-fin.RM",
            name="Risk Management",
            group_name="Quantitative Finance",
            archive_id="q-fin",
            archive_name="Quantitative Finance",
            description="Measurement and management of financial risks in trading, banking, insurance, corporate and other applications",
        )
        ST = Category(
            id="q-fin.ST",
            name="Statistical Finance",
            group_name="Quantitative Finance",
            archive_id="q-fin",
            archive_name="Quantitative Finance",
            description="Statistical, econometric and econophysics analyses with applications to financial markets and economic data",
        )
        TR = Category(
            id="q-fin.TR",
            name="Trading and Market Microstructure",
            group_name="Quantitative Finance",
            archive_id="q-fin",
            archive_name="Quantitative Finance",
            description="Market microstructure, liquidity, exchange and auction design, automated trading, agent-based modeling and market-making",
        )

    @dataclasses.dataclass
    class stat(metaclass=StringableMeta("stat.*")):
        AP = Category(
            id="stat.AP",
            name="Applications",
            group_name="Statistics",
            archive_id="stat",
            archive_name="Statistics",
            description="Biology, Education, Epidemiology, Engineering, Environmental Sciences, Medical, Physical Sciences, Quality Control, Social Sciences",
        )
        CO = Category(
            id="stat.CO",
            name="Computation",
            group_name="Statistics",
            archive_id="stat",
            archive_name="Statistics",
            description="Algorithms, Simulation, Visualization",
        )
        ME = Category(
            id="stat.ME",
            name="Methodology",
            group_name="Statistics",
            archive_id="stat",
            archive_name="Statistics",
            description="Design, Surveys, Model Selection, Multiple Testing, Multivariate Methods, Signal and Image Processing, Time Series, Smoothing, Spatial Statistics, Survival Analysis, Nonparametric and Semiparametric Methods",
        )
        ML = Category(
            id="stat.ML",
            name="Machine Learning",
            group_name="Statistics",
            archive_id="stat",
            archive_name="Statistics",
            description="Covers machine learning papers (supervised, unsupervised, semi-supervised learning, graphical models, reinforcement learning, bandits, high dimensional inference, etc.) with a statistical or theoretical grounding",
        )
        OT = Category(
            id="stat.OT",
            name="Other Statistics",
            group_name="Statistics",
            archive_id="stat",
            archive_name="Statistics",
            description="Work in statistics that does not fit into the other stat classifications",
        )
        TH = Category(
            id="stat.TH",
            name="Statistics Theory",
            group_name="Statistics",
            archive_id="stat",
            archive_name="Statistics",
            description="stat.TH is an alias for math.ST. Asymptotics, Bayesian Inference, Decision Theory, Estimation, Foundations, Inference, Testing.",
        )

    @dataclasses.dataclass
    class astro_ph(metaclass=StringableMeta("astro-ph.*")):
        CO = Category(
            id="astro-ph.CO",
            name="Cosmology and Nongalactic Astrophysics",
            group_name="Physics",
            archive_id="astro-ph",
            archive_name="Astrophysics",
            description="Phenomenology of early universe, cosmic microwave background, cosmological parameters, primordial element abundances, extragalactic distance scale, large-scale structure of the universe. Groups, superclusters, voids, intergalactic medium. Particle astrophysics: dark energy, dark matter, baryogenesis, leptogenesis, inflationary models, reheating, monopoles, WIMPs, cosmic strings, primordial black holes, cosmological gravitational radiation",
        )
        EP = Category(
            id="astro-ph.EP",
            name="Earth and Planetary Astrophysics",
            group_name="Physics",
            archive_id="astro-ph",
            archive_name="Astrophysics",
            description="Interplanetary medium, planetary physics, planetary astrobiology, extrasolar planets, comets, asteroids, meteorites. Structure and formation of the solar system",
        )
        GA = Category(
            id="astro-ph.GA",
            name="Astrophysics of Galaxies",
            group_name="Physics",
            archive_id="astro-ph",
            archive_name="Astrophysics",
            description="Phenomena pertaining to galaxies or the Milky Way. Star clusters, HII regions and planetary nebulae, the interstellar medium, atomic and molecular clouds, dust. Stellar populations. Galactic structure, formation, dynamics. Galactic nuclei, bulges, disks, halo. Active Galactic Nuclei, supermassive black holes, quasars. Gravitational lens systems. The Milky Way and its contents",
        )
        HE = Category(
            id="astro-ph.HE",
            name="High Energy Astrophysical Phenomena",
            group_name="Physics",
            archive_id="astro-ph",
            archive_name="Astrophysics",
            description="Cosmic ray production, acceleration, propagation, detection. Gamma ray astronomy and bursts, X-rays, charged particles, supernovae and other explosive phenomena, stellar remnants and accretion systems, jets, microquasars, neutron stars, pulsars, black holes",
        )
        IM = Category(
            id="astro-ph.IM",
            name="Instrumentation and Methods for Astrophysics",
            group_name="Physics",
            archive_id="astro-ph",
            archive_name="Astrophysics",
            description="Detector and telescope design, experiment proposals. Laboratory Astrophysics. Methods for data analysis, statistical methods. Software, database design",
        )
        SR = Category(
            id="astro-ph.SR",
            name="Solar and Stellar Astrophysics",
            group_name="Physics",
            archive_id="astro-ph",
            archive_name="Astrophysics",
            description="White dwarfs, brown dwarfs, cataclysmic variables. Star formation and protostellar systems, stellar astrobiology, binary and multiple systems of stars, stellar evolution and structure, coronas. Central stars of planetary nebulae. Helioseismology, solar neutrinos, production and detection of gravitational radiation from stellar systems",
        )

    @dataclasses.dataclass
    class cond_mat(metaclass=StringableMeta("cond-mat.*")):
        dis_nn = Category(
            id="cond-mat.dis-nn",
            name="Disordered Systems and Neural Networks",
            group_name="Physics",
            archive_id="cond-mat",
            archive_name="Condensed Matter",
            description="Glasses and spin glasses; properties of random, aperiodic and quasiperiodic systems; transport in disordered media; localization; phenomena mediated by defects and disorder; neural networks",
        )
        mes_hall = Category(
            id="cond-mat.mes-hall",
            name="Mesoscale and Nanoscale Physics",
            group_name="Physics",
            archive_id="cond-mat",
            archive_name="Condensed Matter",
            description="Semiconducting nanostructures: quantum dots, wires, and wells. Single electronics, spintronics, 2d electron gases, quantum Hall effect, nanotubes, graphene, plasmonic nanostructures",
        )
        mtrl_sci = Category(
            id="cond-mat.mtrl-sci",
            name="Materials Science",
            group_name="Physics",
            archive_id="cond-mat",
            archive_name="Condensed Matter",
            description="Techniques, synthesis, characterization, structure. Structural phase transitions, mechanical properties, phonons. Defects, adsorbates, interfaces",
        )
        other = Category(
            id="cond-mat.other",
            name="Other Condensed Matter",
            group_name="Physics",
            archive_id="cond-mat",
            archive_name="Condensed Matter",
            description="Work in condensed matter that does not fit into the other cond-mat classifications",
        )
        quant_gas = Category(
            id="cond-mat.quant-gas",
            name="Quantum Gases",
            group_name="Physics",
            archive_id="cond-mat",
            archive_name="Condensed Matter",
            description="Ultracold atomic and molecular gases, Bose-Einstein condensation, Feshbach resonances, spinor condensates, optical lattices, quantum simulation with cold atoms and molecules, macroscopic interference phenomena",
        )
        soft = Category(
            id="cond-mat.soft",
            name="Soft Condensed Matter",
            group_name="Physics",
            archive_id="cond-mat",
            archive_name="Condensed Matter",
            description="Membranes, polymers, liquid crystals, glasses, colloids, granular matter",
        )
        stat_mech = Category(
            id="cond-mat.stat-mech",
            name="Statistical Mechanics",
            group_name="Physics",
            archive_id="cond-mat",
            archive_name="Condensed Matter",
            description="Phase transitions, thermodynamics, field theory, non-equilibrium phenomena, renormalization group and scaling, integrable models, turbulence",
        )
        str_el = Category(
            id="cond-mat.str-el",
            name="Strongly Correlated Electrons",
            group_name="Physics",
            archive_id="cond-mat",
            archive_name="Condensed Matter",
            description="Quantum magnetism, non-Fermi liquids, spin liquids, quantum criticality, charge density waves, metal-insulator transitions",
        )
        supr_con = Category(
            id="cond-mat.supr-con",
            name="Superconductivity",
            group_name="Physics",
            archive_id="cond-mat",
            archive_name="Condensed Matter",
            description="Superconductivity: theory, models, experiment. Superflow in helium",
        )

    @dataclasses.dataclass
    class nlin(metaclass=StringableMeta("nlin.*")):
        AO = Category(
            id="nlin.AO",
            name="Adaptation and Self-Organizing Systems",
            group_name="Physics",
            archive_id="nlin",
            archive_name="Nonlinear Sciences",
            description="Adaptation, self-organizing systems, statistical physics, fluctuating systems, stochastic processes, interacting particle systems, machine learning",
        )
        CD = Category(
            id="nlin.CD",
            name="Chaotic Dynamics",
            group_name="Physics",
            archive_id="nlin",
            archive_name="Nonlinear Sciences",
            description="Dynamical systems, chaos, quantum chaos, topological dynamics, cycle expansions, turbulence, propagation",
        )
        CG = Category(
            id="nlin.CG",
            name="Cellular Automata and Lattice Gases",
            group_name="Physics",
            archive_id="nlin",
            archive_name="Nonlinear Sciences",
            description="Computational methods, time series analysis, signal processing, wavelets, lattice gases",
        )
        PS = Category(
            id="nlin.PS",
            name="Pattern Formation and Solitons",
            group_name="Physics",
            archive_id="nlin",
            archive_name="Nonlinear Sciences",
            description="Pattern formation, coherent structures, solitons",
        )
        SI = Category(
            id="nlin.SI",
            name="Exactly Solvable and Integrable Systems",
            group_name="Physics",
            archive_id="nlin",
            archive_name="Nonlinear Sciences",
            description="Exactly solvable systems, integrable PDEs, integrable ODEs, Painleve analysis, integrable discrete maps, solvable lattice models, integrable quantum systems",
        )

    @dataclasses.dataclass
    class physics(metaclass=StringableMeta("physics.*")):
        acc_ph = Category(
            id="physics.acc-ph",
            name="Accelerator Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Accelerator theory and simulation. Accelerator technology. Accelerator experiments. Beam Physics. Accelerator design and optimization. Advanced accelerator concepts. Radiation sources including synchrotron light sources and free electron lasers. Applications of accelerators.",
        )
        ao_ph = Category(
            id="physics.ao-ph",
            name="Atmospheric and Oceanic Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Atmospheric and oceanic physics and physical chemistry, biogeophysics, and climate science",
        )
        app_ph = Category(
            id="physics.app-ph",
            name="Applied Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Applications of physics to new technology, including electronic devices, optics, photonics, microwaves, spintronics, advanced materials, metamaterials, nanotechnology, and energy sciences.",
        )
        atm_clus = Category(
            id="physics.atm-clus",
            name="Atomic and Molecular Clusters",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Atomic and molecular clusters, nanoparticles: geometric, electronic, optical, chemical, magnetic properties, shell structure, phase transitions, optical spectroscopy, mass spectrometry, photoelectron spectroscopy, ionization potential, electron affinity, interaction with intense light pulses, electron diffraction, light scattering, ab initio calculations, DFT theory, fragmentation, Coulomb explosion, hydrodynamic expansion.",
        )
        atom_ph = Category(
            id="physics.atom-ph",
            name="Atomic Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Atomic and molecular structure, spectra, collisions, and data. Atoms and molecules in external fields. Molecular dynamics and coherent and optical control. Cold atoms and molecules. Cold collisions. Optical lattices.",
        )
        bio_ph = Category(
            id="physics.bio-ph",
            name="Biological Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Molecular biophysics, cellular biophysics, neurological biophysics, membrane biophysics, single-molecule biophysics, ecological biophysics, quantum phenomena in biological systems (quantum biophysics), theoretical biophysics, molecular dynamics/modeling and simulation, game theory, biomechanics, bioinformatics, microorganisms, virology, evolution, biophysical methods.",
        )
        chem_ph = Category(
            id="physics.chem-ph",
            name="Chemical Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Experimental, computational, and theoretical physics of atoms, molecules, and clusters - Classical and quantum description of states, processes, and dynamics; spectroscopy, electronic structure, conformations, reactions, interactions, and phases. Chemical thermodynamics. Disperse systems. High pressure chemistry. Solid state chemistry. Surface and interface chemistry.",
        )
        class_ph = Category(
            id="physics.class-ph",
            name="Classical Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Newtonian and relativistic dynamics; many particle systems; planetary motions; chaos in classical dynamics. Maxwell's equations and dynamics of charged systems and electromagnetic forces in materials. Vibrating systems such as membranes and cantilevers; optomechanics. Classical waves, including acoustics and elasticity; physics of music and musical instruments. Classical thermodynamics and heat flow problems.",
        )
        comp_ph = Category(
            id="physics.comp-ph",
            name="Computational Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="All aspects of computational science applied to physics.",
        )
        data_an = Category(
            id="physics.data-an",
            name="Data Analysis, Statistics and Probability",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Methods, software and hardware for physics data analysis: data processing and storage; measurement methodology; statistical and mathematical aspects such as parametrization and uncertainties.",
        )
        ed_ph = Category(
            id="physics.ed-ph",
            name="Physics Education",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Report of results of a research study, laboratory experience, assessment or classroom practice that represents a way to improve teaching and learning in physics. Also, report on misconceptions of students, textbook errors, and other similar information relative to promoting physics understanding.",
        )
        flu_dyn = Category(
            id="physics.flu-dyn",
            name="Fluid Dynamics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Turbulence, instabilities, incompressible/compressible flows, reacting flows. Aero/hydrodynamics, fluid-structure interactions, acoustics. Biological fluid dynamics, micro/nanofluidics, interfacial phenomena. Complex fluids, suspensions and granular flows, porous media flows. Geophysical flows, thermoconvective and stratified flows. Mathematical and computational methods for fluid dynamics, fluid flow models, experimental techniques.",
        )
        gen_ph = Category(
            id="physics.gen-ph",
            name="General Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Description coming soon",
        )
        geo_ph = Category(
            id="physics.geo-ph",
            name="Geophysics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Atmospheric physics. Biogeosciences. Computational geophysics. Geographic location. Geoinformatics. Geophysical techniques. Hydrospheric geophysics. Magnetospheric physics. Mathematical geophysics. Planetology. Solar system. Solid earth geophysics. Space plasma physics. Mineral physics. High pressure physics.",
        )
        hist_ph = Category(
            id="physics.hist-ph",
            name="History and Philosophy of Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="History and philosophy of all branches of physics, astrophysics, and cosmology, including appreciations of physicists.",
        )
        ins_det = Category(
            id="physics.ins-det",
            name="Instrumentation and Detectors",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Instrumentation and Detectors for research in natural science, including optical, molecular, atomic, nuclear and particle physics instrumentation and the associated electronics, services, infrastructure and control equipment.",
        )
        med_ph = Category(
            id="physics.med-ph",
            name="Medical Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Radiation therapy. Radiation dosimetry. Biomedical imaging modelling. Reconstruction, processing, and analysis. Biomedical system modelling and analysis. Health physics. New imaging or therapy modalities.",
        )
        optics = Category(
            id="physics.optics",
            name="Optics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Adaptive optics. Astronomical optics. Atmospheric optics. Biomedical optics. Cardinal points. Collimation. Doppler effect. Fiber optics. Fourier optics. Geometrical optics (Gradient index optics. Holography. Infrared optics. Integrated optics. Laser applications. Laser optical systems. Lasers. Light amplification. Light diffraction. Luminescence. Microoptics. Nano optics. Ocean optics. Optical computing. Optical devices. Optical imaging. Optical materials. Optical metrology. Optical microscopy. Optical properties. Optical signal processing. Optical testing techniques. Optical wave propagation. Paraxial optics. Photoabsorption. Photoexcitations. Physical optics. Physiological optics. Quantum optics. Segmented optics. Spectra. Statistical optics. Surface optics. Ultrafast optics. Wave optics. X-ray optics.",
        )
        plasm_ph = Category(
            id="physics.plasm-ph",
            name="Plasma Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Fundamental plasma physics. Magnetically Confined Plasmas (includes magnetic fusion energy research). High Energy Density Plasmas (inertial confinement plasmas, laser-plasma interactions). Ionospheric, Heliophysical, and Astrophysical plasmas (includes sun and solar system plasmas). Lasers, Accelerators, and Radiation Generation. Low temperature plasmas and plasma applications (include dusty plasmas, semiconductor etching, plasma-based nanotechnology, medical applications). Plasma Diagnostics, Engineering and Enabling Technologies (includes fusion reactor design, heating systems, diagnostics, experimental techniques)",
        )
        pop_ph = Category(
            id="physics.pop-ph",
            name="Popular Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Description coming soon",
        )
        soc_ph = Category(
            id="physics.soc-ph",
            name="Physics and Society",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Structure, dynamics and collective behavior of societies and groups (human or otherwise). Quantitative analysis of social networks and other complex networks. Physics and engineering of infrastructure and systems of broad societal impact (e.g., energy grids, transportation networks).",
        )
        space_ph = Category(
            id="physics.space-ph",
            name="Space Physics",
            group_name="Physics",
            archive_id="physics",
            archive_name="Physics",
            description="Space plasma physics. Heliophysics. Space weather. Planetary magnetospheres, ionospheres and magnetotail. Auroras. Interplanetary space. Cosmic rays. Synchrotron radiation. Radio astronomy.",
        )

    gr_qc = Category(
        id="gr-qc",
        name="General Relativity and Quantum Cosmology",
        group_name="Physics",
        archive_id="gr-qc",
        archive_name="General Relativity and Quantum Cosmology",
        description="General Relativity and Quantum Cosmology Areas of gravitational physics, including experiments and observations related to the detection and interpretation of gravitational waves, experimental tests of gravitational theories, computational general relativity, relativistic astrophysics, solutions to Einstein's equations and their properties, alternative theories of gravity, classical and quantum cosmology, and quantum gravity.",
    )
    hep_ex = Category(
        id="hep-ex",
        name="High Energy Physics - Experiment",
        group_name="Physics",
        archive_id="hep-ex",
        archive_name="High Energy Physics - Experiment",
        description="Description coming soon",
    )
    hep_lat = Category(
        id="hep-lat",
        name="High Energy Physics - Lattice",
        group_name="Physics",
        archive_id="hep-lat",
        archive_name="High Energy Physics - Lattice",
        description="Lattice field theory. Phenomenology from lattice field theory. Algorithms for lattice field theory. Hardware for lattice field theory.",
    )
    hep_ph = Category(
        id="hep-ph",
        name="High Energy Physics - Phenomenology",
        group_name="Physics",
        archive_id="hep-ph",
        archive_name="High Energy Physics - Phenomenology",
        description="Theoretical particle physics and its interrelation with experiment. Prediction of particle physics observables: models, effective field theories, calculation techniques. Particle physics: analysis of theory through experimental results.",
    )
    hep_th = Category(
        id="hep-th",
        name="High Energy Physics - Theory",
        group_name="Physics",
        archive_id="hep-th",
        archive_name="High Energy Physics - Theory",
        description="Formal aspects of quantum field theory. String theory, supersymmetry and supergravity.",
    )
    math_ph = Category(
        id="math-ph",
        name="Mathematical Physics",
        group_name="Physics",
        archive_id="math-ph",
        archive_name="Mathematical Physics",
        description="Articles in this category focus on areas of research that illustrate the application of mathematics to problems in physics, develop mathematical methods for such applications, or provide mathematically rigorous formulations of existing physical theories. Submissions to math-ph should be of interest to both physically oriented mathematicians and mathematically oriented physicists; submissions which are primarily of interest to theoretical physicists or to mathematicians should probably be directed to the respective physics/math categories",
    )
    nucl_ex = Category(
        id="nucl-ex",
        name="Nuclear Experiment",
        group_name="Physics",
        archive_id="nucl-ex",
        archive_name="Nuclear Experiment",
        description="Nuclear Experiment Results from experimental nuclear physics including the areas of fundamental interactions, measurements at low- and medium-energy, as well as relativistic heavy-ion collisions. Does not include: detectors and instrumentation nor analysis methods to conduct experiments; descriptions of experimental programs (present or future); comments on published results",
    )
    nucl_th = Category(
        id="nucl-th",
        name="Nuclear Theory",
        group_name="Physics",
        archive_id="nucl-th",
        archive_name="Nuclear Theory",
        description="Nuclear Theory Theory of nuclear structure covering wide area from models of hadron structure to neutron stars. Nuclear equation of states at different external conditions. Theory of nuclear reactions including heavy-ion reactions at low and high energies. It does not include problems of data analysis, physics of nuclear reactors, problems of safety, reactor construction",
    )
    quant_ph = Category(
        id="quant-ph",
        name="Quantum Physics",
        group_name="Physics",
        archive_id="quant-ph",
        archive_name="Quantum Physics",
        description="Description coming soon",
    )


def _get_categories_by_id(root):
    categories_by_id = {}
    for key, obj in root.__dict__.items():
        if key.startswith("_"):
            continue
        if not isinstance(obj, Category):
            # obj is a class-container
            categories_by_id.update(_get_categories_by_id(obj))
        else:
            obj: Category
            categories_by_id[obj.id] = obj
    return categories_by_id


def _get_archives():
    # All fields in Taxonomy corresponds to archives.
    archives = [
        obj for key, obj in Taxonomy.__dict__.items() if not key.startswith("_")
    ]
    return archives


categories_by_id = _get_categories_by_id(Taxonomy)


@dataclasses.dataclass
class Collections:
    # https://blog.arxiv.org/2019/12/05/arxiv-machine-learning-classification-guide/
    machine_learning_broad = [
        Taxonomy.cs.LG,  # Machine Learning
        Taxonomy.stat.ML,  # Machine Learning
        Taxonomy.math.OC,  # Optimization and Control
        Taxonomy.cs.CV,  # Computer Vision and Pattern Recognition
        Taxonomy.cs.CL,  # Computation and Language
        Taxonomy.eess.AS,  # Audio and Speech Processing
        Taxonomy.cs.IR,  # Information Retrieval
        Taxonomy.cs.HC,  # Human-Computer Interaction
        Taxonomy.cs.SI,  # Social and Information Networks
        Taxonomy.cs.CY,  # Computers and Society
        Taxonomy.cs.GR,  # Graphics
        Taxonomy.cs.SY,  # Systems and Control
        Taxonomy.cs.AI,  # Artificial Intelligence
        Taxonomy.cs.MM,  # Multimedia
        Taxonomy.cs.ET,  # Emerging Technologies
        Taxonomy.cs.NE,  # Neural and Evolutionary Computing
    ]
    hep = [
        Taxonomy.hep_th,
        Taxonomy.hep_ph,
        Taxonomy.hep_ex,
        Taxonomy.hep_lat,
    ]
    all_categories = list(categories_by_id.values())
    all_archives = _get_archives()


__all__ = ["Taxonomy", "Category", "Collections", "categories_by_id"]
