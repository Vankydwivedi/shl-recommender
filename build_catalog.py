"""
Generate catalog.json from scraped SHL catalog data.
Run: python build_catalog.py
"""

import json
from pathlib import Path

BASE_URL = "https://www.shl.com"

RAW_ITEMS = [
  # Page 0 (start=0)
  {"name":"Global Skills Development Report","url":"/products/product-catalog/view/global-skills-development-report/","test_types":["A","E","B","C","D","P"]},
  {"name":".NET Framework 4.5","url":"/products/product-catalog/view/net-framework-4-5/","test_types":["K"]},
  {"name":".NET MVC (New)","url":"/products/product-catalog/view/net-mvc-new/","test_types":["K"]},
  {"name":".NET MVVM (New)","url":"/products/product-catalog/view/net-mvvm-new/","test_types":["K"]},
  {"name":".NET WCF (New)","url":"/products/product-catalog/view/net-wcf-new/","test_types":["K"]},
  {"name":".NET WPF (New)","url":"/products/product-catalog/view/net-wpf-new/","test_types":["K"]},
  {"name":".NET XAML (New)","url":"/products/product-catalog/view/net-xaml-new/","test_types":["K"]},
  {"name":"Accounts Payable (New)","url":"/products/product-catalog/view/accounts-payable-new/","test_types":["K"]},
  {"name":"Accounts Payable Simulation (New)","url":"/products/product-catalog/view/accounts-payable-simulation-new/","test_types":["S"]},
  {"name":"Accounts Receivable (New)","url":"/products/product-catalog/view/accounts-receivable-new/","test_types":["K"]},
  {"name":"Accounts Receivable Simulation (New)","url":"/products/product-catalog/view/accounts-receivable-simulation-new/","test_types":["S"]},
  {"name":"ADO.NET (New)","url":"/products/product-catalog/view/ado-net-new/","test_types":["K"]},
  # Page 1 (start=12)
  {"name":"Adobe Experience Manager (New)","url":"/products/product-catalog/view/adobe-experience-manager-new/","test_types":["K"]},
  {"name":"Adobe Photoshop CC","url":"/products/product-catalog/view/adobe-photoshop-cc/","test_types":["K"]},
  {"name":"Aeronautical Engineering (New)","url":"/products/product-catalog/view/aeronautical-engineering-new/","test_types":["K"]},
  {"name":"Aerospace Engineering (New)","url":"/products/product-catalog/view/aerospace-engineering-new/","test_types":["K"]},
  {"name":"Agile Software Development","url":"/products/product-catalog/view/agile-software-development/","test_types":["K"]},
  {"name":"Agile Testing (New)","url":"/products/product-catalog/view/agile-testing-new/","test_types":["K"]},
  {"name":"AI Skills","url":"/products/product-catalog/view/ai-skills/","test_types":["P"]},
  {"name":"Amazon Web Services (AWS) Development (New)","url":"/products/product-catalog/view/amazon-web-services-aws-development-new/","test_types":["K"]},
  {"name":"Android Development (New)","url":"/products/product-catalog/view/android-development-new/","test_types":["K"]},
  {"name":"Angular 6 (New)","url":"/products/product-catalog/view/angular-6-new/","test_types":["K"]},
  {"name":"AngularJS (New)","url":"/products/product-catalog/view/angularjs-new/","test_types":["K"]},
  {"name":"Apache Hadoop (New)","url":"/products/product-catalog/view/apache-hadoop-new/","test_types":["K"]},
  # Page 2 (start=24)
  {"name":"Apache Hadoop Extensions (New)","url":"/products/product-catalog/view/apache-hadoop-extensions-new/","test_types":["K"]},
  {"name":"Apache HBase (New)","url":"/products/product-catalog/view/apache-hbase-new/","test_types":["K"]},
  {"name":"Apache Hive (New)","url":"/products/product-catalog/view/apache-hive-new/","test_types":["K"]},
  {"name":"Apache Kafka (New)","url":"/products/product-catalog/view/apache-kafka-new/","test_types":["K"]},
  {"name":"Apache Pig (New)","url":"/products/product-catalog/view/apache-pig-new/","test_types":["K"]},
  {"name":"Apache Spark (New)","url":"/products/product-catalog/view/apache-spark-new/","test_types":["K"]},
  {"name":"ASP .NET with C# (New)","url":"/products/product-catalog/view/asp-net-with-c-new/","test_types":["K"]},
  {"name":"ASP.NET 4.5","url":"/products/product-catalog/view/asp-net-4-5/","test_types":["K"]},
  {"name":"Assessment and Development Center Exercises","url":"/products/product-catalog/view/assessment-and-development-center-exercises/","test_types":["E"]},
  {"name":"Automata - Fix (New)","url":"/products/product-catalog/view/automata-fix-new/","test_types":["S"]},
  {"name":"Automata - SQL (New)","url":"/products/product-catalog/view/automata-sql-new/","test_types":["S"]},
  {"name":"Automata (New)","url":"/products/product-catalog/view/automata-new/","test_types":["S"]},
  # Page 3 (start=36)
  {"name":"Automata Data Science (New)","url":"/products/product-catalog/view/automata-data-science-new/","test_types":["S"]},
  {"name":"Automata Data Science Pro (New)","url":"/products/product-catalog/view/automata-data-science-pro-new/","test_types":["S"]},
  {"name":"Automata Front End","url":"/products/product-catalog/view/automata-front-end/","test_types":["S"]},
  {"name":"Automata Pro (New)","url":"/products/product-catalog/view/automata-pro-new/","test_types":["S"]},
  {"name":"Automata Selenium","url":"/products/product-catalog/view/automata-selenium/","test_types":["S"]},
  {"name":"Automation Anywhere RPA Development (New)","url":"/products/product-catalog/view/automation-anywhere-rpa-development-new/","test_types":["K"]},
  {"name":"Automotive Engineering (New)","url":"/products/product-catalog/view/automotive-engineering-new/","test_types":["K"]},
  {"name":"Basic Biology (New)","url":"/products/product-catalog/view/basic-biology-new/","test_types":["K"]},
  {"name":"Basic Computer Literacy (Windows 10) (New)","url":"/products/product-catalog/view/basic-computer-literacy-windows-10-new/","test_types":["S","K"]},
  {"name":"Basic Statistics (New)","url":"/products/product-catalog/view/basic-statistics-new/","test_types":["K"]},
  {"name":"Biochemistry (New)","url":"/products/product-catalog/view/biochemistry-new/","test_types":["K"]},
  {"name":"Biotech Lab Techniques (New)","url":"/products/product-catalog/view/biotech-lab-techniques-new/","test_types":["K"]},
  # Page 4 (start=48)
  {"name":"BizTalk (New)","url":"/products/product-catalog/view/biztalk-new/","test_types":["K"]},
  {"name":"Business Communication (adaptive)","url":"/products/product-catalog/view/business-communication-adaptive/","test_types":["K"]},
  {"name":"Business Communications","url":"/products/product-catalog/view/business-communications/","test_types":["K"]},
  {"name":"C Programming (New)","url":"/products/product-catalog/view/c-programming-new/","test_types":["K"]},
  {"name":"C# Programming (New)","url":"/products/product-catalog/view/c-programming-new-4039/","test_types":["K"]},
  {"name":"C++ Programming (New)","url":"/products/product-catalog/view/c-programming-new-4122/","test_types":["K"]},
  {"name":"Cardiology and Diabetes Management (New)","url":"/products/product-catalog/view/cardiology-and-diabetes-management-new/","test_types":["K"]},
  {"name":"Ceramic Engineering (New)","url":"/products/product-catalog/view/ceramic-engineering-new/","test_types":["K"]},
  {"name":"Chemical Engineering (New)","url":"/products/product-catalog/view/chemical-engineering-new/","test_types":["K"]},
  {"name":"Cisco AppDynamics (New)","url":"/products/product-catalog/view/cisco-appdynamics-new/","test_types":["K"]},
  {"name":"Civil Engineering (New)","url":"/products/product-catalog/view/civil-engineering-new/","test_types":["K"]},
  {"name":"Cloud Computing (New)","url":"/products/product-catalog/view/cloud-computing-new/","test_types":["K"]},
  # Page 5 (start=60)
  {"name":"COBOL Programming (New)","url":"/products/product-catalog/view/cobol-programming-new/","test_types":["K"]},
  {"name":"Computer Science (New)","url":"/products/product-catalog/view/computer-science-new/","test_types":["K"]},
  {"name":"Contact Center Call Simulation (New)","url":"/products/product-catalog/view/contact-center-call-simulation-new/","test_types":["S"]},
  {"name":"Conversational Multichat Simulation","url":"/products/product-catalog/view/conversational-multichat-simulation/","test_types":["S"]},
  {"name":"Core Java (Advanced Level) (New)","url":"/products/product-catalog/view/core-java-advanced-level-new/","test_types":["K"]},
  {"name":"Core Java (Entry Level) (New)","url":"/products/product-catalog/view/core-java-entry-level-new/","test_types":["K"]},
  {"name":"Count Out The Money","url":"/products/product-catalog/view/count-out-the-money/","test_types":["K","S"]},
  {"name":"CSS3 (New)","url":"/products/product-catalog/view/css3-new/","test_types":["K"]},
  {"name":"Culinary Skills (New)","url":"/products/product-catalog/view/culinary-skills-new/","test_types":["K"]},
  {"name":"Customer Service Phone Simulation","url":"/products/product-catalog/view/customer-service-phone-simulation/","test_types":["B","S"]},
  {"name":"Customer Service Phone Solution","url":"/products/product-catalog/view/customer-service-phone-solution/","test_types":["B","P","S"]},
  {"name":"Cyber Risk (New)","url":"/products/product-catalog/view/cyber-risk-new/","test_types":["K"]},
  # Page 6 (start=72)
  {"name":"Data Entry (New)","url":"/products/product-catalog/view/data-entry-new/","test_types":["S"]},
  {"name":"Data Entry Alphanumeric Split Screen - US","url":"/products/product-catalog/view/data-entry-alphanumeric-split-screen-us/","test_types":["K"]},
  {"name":"Data Entry Numeric Split Screen - US","url":"/products/product-catalog/view/data-entry-numeric-split-screen-us/","test_types":["K"]},
  {"name":"Data Entry Ten Key Split Screen","url":"/products/product-catalog/view/data-entry-ten-key-split-screen/","test_types":["K"]},
  {"name":"Data Science (New)","url":"/products/product-catalog/view/data-science-new/","test_types":["K"]},
  {"name":"Data Warehousing Concepts","url":"/products/product-catalog/view/data-warehousing-concepts/","test_types":["K"]},
  {"name":"Dependability and Safety Instrument (DSI)","url":"/products/product-catalog/view/dependability-and-safety-instrument-dsi/","test_types":["P"]},
  {"name":"Dermatology (New)","url":"/products/product-catalog/view/dermatology-new/","test_types":["K"]},
  {"name":"Desktop Support (New)","url":"/products/product-catalog/view/desktop-support-new/","test_types":["K"]},
  {"name":"Digital Advertising (New)","url":"/products/product-catalog/view/digital-advertising-new/","test_types":["K"]},
  {"name":"Digital Readiness Development Report - IC","url":"/products/product-catalog/view/digital-readiness-development-report/","test_types":["P"]},
  {"name":"Digital Readiness Development Report - Manager","url":"/products/product-catalog/view/digital-readiness-development-report-manager/","test_types":["P"]},
  # Page 7 (start=84)
  {"name":"Docker (New)","url":"/products/product-catalog/view/docker-new/","test_types":["K"]},
  {"name":"Dojo (New)","url":"/products/product-catalog/view/dojo-new/","test_types":["K"]},
  {"name":"Drupal (New)","url":"/products/product-catalog/view/drupal-new/","test_types":["K"]},
  {"name":"DSI v1.1 Interpretation Report","url":"/products/product-catalog/view/dsi-v1-1-interpretation-report/","test_types":["P"]},
  {"name":"Econometrics (New)","url":"/products/product-catalog/view/econometrics-new/","test_types":["K"]},
  {"name":"Economics (New)","url":"/products/product-catalog/view/economics-new/","test_types":["K"]},
  {"name":"Electrical and Electronics Engineering (New)","url":"/products/product-catalog/view/electrical-and-electronics-engineering-new/","test_types":["K"]},
  {"name":"Electrical Engineering (New)","url":"/products/product-catalog/view/electrical-engineering-new/","test_types":["K"]},
  {"name":"Electronics & Telecommunications Engineering (New)","url":"/products/product-catalog/view/electronics-and-telecommunications-engineering-new/","test_types":["K"]},
  {"name":"Electronics and Embedded Systems Engineering (New)","url":"/products/product-catalog/view/electronics-and-embedded-systems-engineering-new/","test_types":["K"]},
  {"name":"Electronics and Semiconductor Engineering (New)","url":"/products/product-catalog/view/electronics-and-semiconductor-engineering-new/","test_types":["K"]},
  {"name":"English Comprehension (New)","url":"/products/product-catalog/view/english-comprehension-new/","test_types":["K"]},
  # Page 8 (start=96)
  {"name":"Enterprise Java Beans (New)","url":"/products/product-catalog/view/enterprise-java-beans-new/","test_types":["K"]},
  {"name":"Enterprise Leadership Report 1.0","url":"/products/product-catalog/view/enterprise-leadership-report/","test_types":["P"]},
  {"name":"Enterprise Leadership Report 2.0","url":"/products/product-catalog/view/enterprise-leadership-report-2-0/","test_types":["P"]},
  {"name":"Entry Level Cashier Solution","url":"/products/product-catalog/view/entry-level-cashier-solution/","test_types":["C","P"]},
  {"name":"Entry Level Customer Serv-Retail & Contact Center","url":"/products/product-catalog/view/entry-level-customer-serv-retail-and-contact-center/","test_types":["P","C"]},
  {"name":"Entry Level Customer Service (General) Solution","url":"/products/product-catalog/view/entry-level-customer-service-general-solution/","test_types":["C","P"]},
  {"name":"Entry Level Hotel Front Desk Solution","url":"/products/product-catalog/view/entry-level-hotel-front-desk-solution/","test_types":["C","P"]},
  {"name":"Entry Level Sales Solution","url":"/products/product-catalog/view/entry-level-sales-solution/","test_types":["C","P"]},
  {"name":"Entry Level Technical Support Solution","url":"/products/product-catalog/view/entry-level-technical-support-solution/","test_types":["P","C"]},
  {"name":"ETL Testing (New)","url":"/products/product-catalog/view/etl-testing-new/","test_types":["K"]},
  {"name":"Executive Scenarios","url":"/products/product-catalog/view/executive-scenarios/","test_types":["B"]},
  {"name":"Executive Scenarios Narrative Report","url":"/products/product-catalog/view/executive-scenarios-narrative-report/","test_types":["B"]},
  # Page 9 (start=108)
  {"name":"Executive Scenarios Profile Report","url":"/products/product-catalog/view/executive-scenarios-profile-report/","test_types":["B"]},
  {"name":"ExpressJS (New)","url":"/products/product-catalog/view/expressjs-new/","test_types":["K"]},
  {"name":"Filing - Names (R1)","url":"/products/product-catalog/view/filing-names-r1/","test_types":["K"]},
  {"name":"Filing - Numbers","url":"/products/product-catalog/view/filing-numbers/","test_types":["K"]},
  {"name":"Financial Accounting (New)","url":"/products/product-catalog/view/financial-accounting-new/","test_types":["K"]},
  {"name":"Financial and Banking Services (New)","url":"/products/product-catalog/view/financial-and-banking-services-new/","test_types":["K"]},
  {"name":"Fire Engineering (New)","url":"/products/product-catalog/view/fire-engineering-new/","test_types":["K"]},
  {"name":"Following Instructions v1 - UK (R1)","url":"/products/product-catalog/view/following-instructions-v1-uk-r1/","test_types":["K"]},
  {"name":"Following Instructions v1 - US (R2)","url":"/products/product-catalog/view/following-instructions-v1-us-r2/","test_types":["K"]},
  {"name":"Food and Beverage Services (New)","url":"/products/product-catalog/view/food-and-beverage-services-new/","test_types":["K"]},
  {"name":"Food Science (New)","url":"/products/product-catalog/view/food-science-new/","test_types":["K"]},
  {"name":"Front Office Management (New)","url":"/products/product-catalog/view/front-office-management-new/","test_types":["K"]},
  # Page 10 (start=120)
  {"name":"Fundamentals of Chemistry (New)","url":"/products/product-catalog/view/fundamentals-of-chemistry-new/","test_types":["K"]},
  {"name":"Fundamentals of Physics (New)","url":"/products/product-catalog/view/fundamentals-of-physics-new/","test_types":["K"]},
  {"name":"General Diseases (New)","url":"/products/product-catalog/view/general-diseases-new/","test_types":["K"]},
  {"name":"Geoinformatics Engineering (New)","url":"/products/product-catalog/view/geoinformatics-engineering-new/","test_types":["K"]},
  {"name":"Geoscience Engineering (New)","url":"/products/product-catalog/view/geoscience-engineering-new/","test_types":["K"]},
  {"name":"GIT (New)","url":"/products/product-catalog/view/git-new/","test_types":["K"]},
  {"name":"Global Skills Assessment","url":"/products/product-catalog/view/global-skills-assessment/","test_types":["C","K"]},
  {"name":"Graduate Scenarios","url":"/products/product-catalog/view/graduate-scenarios/","test_types":["B"]},
  {"name":"Graduate Scenarios Narrative Report","url":"/products/product-catalog/view/graduate-scenarios-narrative-report/","test_types":["B"]},
  {"name":"Graduate Scenarios Profile Report","url":"/products/product-catalog/view/graduate-scenarios-profile-report/","test_types":["B"]},
  {"name":"Hibernate (New)","url":"/products/product-catalog/view/hibernate-new/","test_types":["K"]},
  {"name":"HIPAA (Security)","url":"/products/product-catalog/view/hipaa-security/","test_types":["K"]},
  # Page 11 (start=132)
  {"name":"HiPo Assessment Report 1.0","url":"/products/product-catalog/view/hipo-assessment-report-1-0/","test_types":["C","P"]},
  {"name":"HiPo Assessment Report 2.0","url":"/products/product-catalog/view/hipo-assessment-report-2-0/","test_types":["C","P"]},
  {"name":"HiPo Unlocking Potential Report 2.0","url":"/products/product-catalog/view/hipo-unlocking-potential-report-2-0/","test_types":["C"]},
  {"name":"Housekeeping (New)","url":"/products/product-catalog/view/housekeeping-new/","test_types":["K"]},
  {"name":"HTML/CSS (New)","url":"/products/product-catalog/view/htmlcss-new/","test_types":["K"]},
  {"name":"HTML5 (New)","url":"/products/product-catalog/view/html5-new/","test_types":["K"]},
  {"name":"Human Resources (New)","url":"/products/product-catalog/view/human-resources-new/","test_types":["K"]},
  {"name":"IBM DataStage (New)","url":"/products/product-catalog/view/ibm-datastage-new/","test_types":["K"]},
  {"name":"IBM Sterling Order Management System (New)","url":"/products/product-catalog/view/ibm-sterling-order-management-system-new/","test_types":["K"]},
  {"name":"Industrial Engineering (New)","url":"/products/product-catalog/view/industrial-engineering-new/","test_types":["K"]},
  {"name":"Informatica (Architecture) (New)","url":"/products/product-catalog/view/informatica-architecture-new/","test_types":["K"]},
  {"name":"Informatica (Developer) (New)","url":"/products/product-catalog/view/informatica-developer-new/","test_types":["K"]},
  # Page 12 (start=144)
  {"name":"Instrumentation Engineering (New)","url":"/products/product-catalog/view/instrumentation-engineering-new/","test_types":["K"]},
  {"name":"Interpersonal Communications","url":"/products/product-catalog/view/interpersonal-communications/","test_types":["K"]},
  {"name":"Interviewing and Hiring Concepts (U.S.)","url":"/products/product-catalog/view/interviewing-and-hiring-concepts-u-s/","test_types":["K"]},
  {"name":"iOS Development (New)","url":"/products/product-catalog/view/ios-development-new/","test_types":["K"]},
  {"name":"ITIL (IT Infrastructure Library) (New)","url":"/products/product-catalog/view/itil-it-infrastructure-library-new/","test_types":["K"]},
  {"name":"Java 2 Platform Enterprise Edition 1.4 Fundamental","url":"/products/product-catalog/view/java-2-platform-enterprise-edition-1-4-fundamental/","test_types":["K"]},
  {"name":"Java 8 (New)","url":"/products/product-catalog/view/java-8-new/","test_types":["K"]},
  {"name":"Java Design Patterns (New)","url":"/products/product-catalog/view/java-design-patterns-new/","test_types":["K"]},
  {"name":"Java Frameworks (New)","url":"/products/product-catalog/view/java-frameworks-new/","test_types":["K"]},
  {"name":"Java Platform Enterprise Edition 7 (Java EE 7)","url":"/products/product-catalog/view/java-platform-enterprise-edition-7-java-ee-7/","test_types":["K"]},
  {"name":"Java Web Services (New)","url":"/products/product-catalog/view/java-web-services-new/","test_types":["K"]},
  {"name":"JavaScript (New)","url":"/products/product-catalog/view/javascript-new/","test_types":["K"]},
  # Page 13 (start=156)
  {"name":"Jenkins (New)","url":"/products/product-catalog/view/jenkins-new/","test_types":["K"]},
  {"name":"Job Control Language (New)","url":"/products/product-catalog/view/job-control-language-new/","test_types":["K"]},
  {"name":"jQuery (New)","url":"/products/product-catalog/view/jquery-new/","test_types":["K"]},
  {"name":"Kubernetes (New)","url":"/products/product-catalog/view/kubernetes-new/","test_types":["K"]},
  {"name":"Linux Administration (New)","url":"/products/product-catalog/view/linux-administration-new/","test_types":["K"]},
  {"name":"Linux Operating System","url":"/products/product-catalog/view/linux-operating-system/","test_types":["K"]},
  {"name":"Linux Programming (General)","url":"/products/product-catalog/view/linux-programming-general/","test_types":["K"]},
  {"name":"Load Runner (New)","url":"/products/product-catalog/view/load-runner-new/","test_types":["K"]},
  {"name":"Management Scenarios","url":"/products/product-catalog/view/management-scenarios/","test_types":["B"]},
  {"name":"Managerial Scenarios Candidate Report","url":"/products/product-catalog/view/managerial-scenarios-candidate-report/","test_types":["B"]},
  {"name":"Managerial Scenarios Narrative Report","url":"/products/product-catalog/view/managerial-scenarios-narrative-report/","test_types":["B"]},
  {"name":"Managerial Scenarios Profile Report","url":"/products/product-catalog/view/managerial-scenarios-profile-report/","test_types":["B"]},
  # Page 14 (start=168)
  {"name":"Manual Testing (New)","url":"/products/product-catalog/view/manual-testing-new/","test_types":["K"]},
  {"name":"Manufac. & Indust. - Mechanical & Vigilance 8.0","url":"/products/product-catalog/view/mechanical-and-vigilance-focus-8-0/","test_types":["A","P"]},
  {"name":"Manufac. & Indust. - Safety & Dependability 8.0","url":"/products/product-catalog/view/safety-and-dependability-focus-8-0/","test_types":["P"]},
  {"name":"Manufacturing & Industrial - Essential Focus 8.0","url":"/products/product-catalog/view/essential-focus-8-0/","test_types":["P"]},
  {"name":"Manufacturing & Industrial - Mechanical Focus 8.0","url":"/products/product-catalog/view/mechanical-focus-8-0/","test_types":["A","P"]},
  {"name":"Manufacturing & Industrial - Vigilance Focus 8.0","url":"/products/product-catalog/view/vigilance-focus-8-0/","test_types":["A","P"]},
  {"name":"Marketing (New)","url":"/products/product-catalog/view/marketing-new/","test_types":["K"]},
  {"name":"Maven (New)","url":"/products/product-catalog/view/maven-new/","test_types":["K"]},
  {"name":"Mechanical Engineering (New)","url":"/products/product-catalog/view/mechanical-engineering-new/","test_types":["K"]},
  {"name":"Mechatronics Engineering (New)","url":"/products/product-catalog/view/mechatronics-engineering-new/","test_types":["K"]},
  {"name":"Medical Terminology (New)","url":"/products/product-catalog/view/medical-terminology-new/","test_types":["K"]},
  {"name":"Metallurgical Engineering (New)","url":"/products/product-catalog/view/metallurgical-engineering-new/","test_types":["K"]},
  # Page 15 (start=180)
  {"name":"MFS 360 Enterprise Leadership Report","url":"/products/product-catalog/view/mfs-360-enterprise-leadership-report/","test_types":["D"]},
  {"name":"MFS 360 UCF Group Report","url":"/products/product-catalog/view/mfs-360-ucf-group-report/","test_types":["D"]},
  {"name":"MFS 360 UCF Performance Potential Dev Tips Report","url":"/products/product-catalog/view/mfs-360-ucf-performance-potential-dev-tips-report/","test_types":["D"]},
  {"name":"MFS 360 UCF Standard Report","url":"/products/product-catalog/view/mfs-360-ucf-standard-report/","test_types":["D"]},
  {"name":"Micro Focus Unified Functional Testing (New)","url":"/products/product-catalog/view/micro-focus-unified-functional-testing-new/","test_types":["K"]},
  {"name":"Microservices (New)","url":"/products/product-catalog/view/microservices-new/","test_types":["K"]},
  {"name":"Microsoft Dynamics Development (New)","url":"/products/product-catalog/view/microsoft-dynamics-development-new/","test_types":["K"]},
  {"name":"Microsoft Excel 365 - Essentials (New)","url":"/products/product-catalog/view/microsoft-excel-365-essentials-new/","test_types":["K","S"]},
  {"name":"Microsoft Excel 365 (New)","url":"/products/product-catalog/view/microsoft-excel-365-new/","test_types":["K","S"]},
  {"name":"Microsoft Outlook 2013 (adaptive)","url":"/products/product-catalog/view/microsoft-outlook-2013-adaptive/","test_types":["K"]},
  {"name":"Microsoft PowerPoint 365 - Essentials (New)","url":"/products/product-catalog/view/microsoft-powerpoint-365-essentials-new/","test_types":["K","S"]},
  {"name":"Microsoft SQL Server 2014 Programming","url":"/products/product-catalog/view/microsoft-sql-server-2014-programming/","test_types":["K"]},
  # Page 16 (start=192)
  {"name":"Microsoft Windows Server 2012 Administration","url":"/products/product-catalog/view/microsoft-windows-server-2012-administration/","test_types":["K"]},
  {"name":"Microsoft Word 365 - Essentials (New)","url":"/products/product-catalog/view/microsoft-word-365-essentials-new/","test_types":["K","S"]},
  {"name":"Microsoft Word 365 (New)","url":"/products/product-catalog/view/microsoft-word-365-new/","test_types":["S","K"]},
  {"name":"Mineral Engineering (New)","url":"/products/product-catalog/view/mineral-engineering-new/","test_types":["K"]},
  {"name":"Mining Engineering (New)","url":"/products/product-catalog/view/mining-engineering-new/","test_types":["K"]},
  {"name":"Mobility (New)","url":"/products/product-catalog/view/mobility-new/","test_types":["K"]},
  {"name":"Molecular Biology (New)","url":"/products/product-catalog/view/molecular-biology-new/","test_types":["K"]},
  {"name":"MongoDB (New)","url":"/products/product-catalog/view/mongodb-new/","test_types":["K"]},
  {"name":"Motivation Questionnaire MQM5","url":"/products/product-catalog/view/motivation-questionnaire-mqm5/","test_types":["P"]},
  {"name":"MQ Candidate Motivation Report","url":"/products/product-catalog/view/mq-candidate-motivation-report/","test_types":["P"]},
  {"name":"MQ Employee Motivation Report","url":"/products/product-catalog/view/mq-employee-motivation-report/","test_types":["P"]},
  {"name":"MQ Motivation Report Pack","url":"/products/product-catalog/view/mq-motivation-report-pack/","test_types":["P"]},
  # Page 17 (start=204)
  {"name":"MQ Profile","url":"/products/product-catalog/view/mq-profile/","test_types":["P"]},
  {"name":"MS Access (New)","url":"/products/product-catalog/view/ms-access-new/","test_types":["K"]},
  {"name":"MS Excel (New)","url":"/products/product-catalog/view/ms-excel-new/","test_types":["K"]},
  {"name":"MS Office Basic Computer Literacy (New)","url":"/products/product-catalog/view/ms-office-basic-computer-literacy-new/","test_types":["K"]},
  {"name":"MS Office Basic Computer Literacy (Sim) (New)","url":"/products/product-catalog/view/ms-office-basic-computer-literacy-sim-new/","test_types":["S"]},
  {"name":"MS PowerPoint (New)","url":"/products/product-catalog/view/ms-powerpoint-new/","test_types":["K"]},
  {"name":"MS Word (New)","url":"/products/product-catalog/view/ms-word-new/","test_types":["K"]},
  {"name":"MuleSoft Development (New)","url":"/products/product-catalog/view/mulesoft-development-new/","test_types":["K"]},
  {"name":"Multitasking Ability","url":"/products/product-catalog/view/multitasking-ability/","test_types":["A","K","S"]},
  {"name":"Networking and Implementation (New)","url":"/products/product-catalog/view/networking-and-implementation-new/","test_types":["K"]},
  {"name":"Node.js (New)","url":"/products/product-catalog/view/node-js-new/","test_types":["K"]},
  {"name":"Nursing (New)","url":"/products/product-catalog/view/nursing-new/","test_types":["K"]},
  # Page 18 (start=216)
  {"name":"Occupational Personality Questionnaire OPQ32r","url":"/products/product-catalog/view/occupational-personality-questionnaire-opq32r/","test_types":["P"]},
  {"name":"Operations Management (New)","url":"/products/product-catalog/view/operations-management-new/","test_types":["K"]},
  {"name":"OPQ Candidate Plus Report","url":"/products/product-catalog/view/opq-candidate-plus-report/","test_types":["P"]},
  {"name":"OPQ Candidate Report 2.0","url":"/products/product-catalog/view/opq-candidate-report-2-0/","test_types":["P"]},
  {"name":"OPQ Emotional Intelligence Report","url":"/products/product-catalog/view/opq-emotional-intelligence-report/","test_types":["P"]},
  {"name":"OPQ Leadership Report","url":"/products/product-catalog/view/opq-leadership-report/","test_types":["P"]},
  {"name":"OPQ Manager Plus Report","url":"/products/product-catalog/view/opq-manager-plus-report/","test_types":["P"]},
  {"name":"OPQ Manager Plus Report 2.0","url":"/products/product-catalog/view/opq-manager-plus-report-2-0/","test_types":["P"]},
  {"name":"OPQ Maximising your Learning Report","url":"/products/product-catalog/view/opq-maximising-your-learning-report/","test_types":["P"]},
  {"name":"OPQ MQ Sales Report","url":"/products/product-catalog/view/opq-mq-sales-report/","test_types":["P"]},
  {"name":"OPQ Premium Plus Report","url":"/products/product-catalog/view/opq-premium-plus-report/","test_types":["P"]},
  {"name":"OPQ Premium Plus Report 2.0","url":"/products/product-catalog/view/opq-premium-plus-report-2-0/","test_types":["P"]},
  # Page 19 (start=228)
  {"name":"OPQ Profile Report","url":"/products/product-catalog/view/opq-profile-report/","test_types":["P"]},
  {"name":"OPQ Team Impact Group Development Report","url":"/products/product-catalog/view/opq-team-impact-group-development-report/","test_types":["P"]},
  {"name":"OPQ Team Impact Individual Development Report","url":"/products/product-catalog/view/opq-team-impact-individual-development-report/","test_types":["P"]},
  {"name":"OPQ Team Impact Selection Report","url":"/products/product-catalog/view/opq-team-impact-selection-report/","test_types":["P"]},
  {"name":"OPQ Team Types & Leadership Styles Profile","url":"/products/product-catalog/view/opq-team-types-and-leadership-styles-profile/","test_types":["P"]},
  {"name":"OPQ Team Types and Leadership Styles Report","url":"/products/product-catalog/view/opq-team-types-and-leadership-styles-report/","test_types":["P"]},
  {"name":"OPQ UCF Development Action Planner Report 1.0","url":"/products/product-catalog/view/opq-ucf-development-action-planner-report/","test_types":["P"]},
  {"name":"OPQ UCF Development Action Planner Report 2.0","url":"/products/product-catalog/view/opq-ucf-development-action-planner-report-2-0/","test_types":["P"]},
  {"name":"OPQ Universal Competency Report 1.0","url":"/products/product-catalog/view/opq-universal-competency-report/","test_types":["P"]},
  {"name":"OPQ Universal Competency Report 2.0","url":"/products/product-catalog/view/opq-universal-competency-report-2-0/","test_types":["P"]},
  {"name":"OPQ User and Managers Report","url":"/products/product-catalog/view/opq-user-and-managers-report/","test_types":["P"]},
  {"name":"OPQ User Report","url":"/products/product-catalog/view/opq-user-report/","test_types":["P","S"]},
  # Page 20 (start=240)
  {"name":"Oracle DBA (Advanced Level) (New)","url":"/products/product-catalog/view/oracle-dba-advanced-level-new/","test_types":["K"]},
  {"name":"Oracle DBA (Entry Level) (New)","url":"/products/product-catalog/view/oracle-dba-entry-level-new/","test_types":["K"]},
  {"name":"Oracle PL/SQL (New)","url":"/products/product-catalog/view/oracle-plsql-new/","test_types":["K"]},
  {"name":"Oracle WebLogic Server (New)","url":"/products/product-catalog/view/oracle-weblogic-server-new/","test_types":["K"]},
  {"name":"Organic Chemistry (New)","url":"/products/product-catalog/view/organic-chemistry-new/","test_types":["K"]},
  {"name":"Paint Technology (New)","url":"/products/product-catalog/view/paint-technology-new/","test_types":["K"]},
  {"name":"Pediatrics (New)","url":"/products/product-catalog/view/pediatrics-new/","test_types":["K"]},
  {"name":"Pega Development (New)","url":"/products/product-catalog/view/pega-development-new/","test_types":["K"]},
  {"name":"Perl (New)","url":"/products/product-catalog/view/perl-new/","test_types":["K"]},
  {"name":"Petrochemical Engineering (New)","url":"/products/product-catalog/view/petrochemical-engineering-new/","test_types":["K"]},
  {"name":"Petroleum Engineering (New)","url":"/products/product-catalog/view/petroleum-engineering-new/","test_types":["K"]},
  {"name":"Pharmaceutical Analysis (New)","url":"/products/product-catalog/view/pharmaceutical-analysis-new/","test_types":["K"]},
  # Page 21 (start=252)
  {"name":"Pharmaceutical Chemistry (New)","url":"/products/product-catalog/view/pharmaceutical-chemistry-new/","test_types":["K"]},
  {"name":"Pharmaceutical Science (New)","url":"/products/product-catalog/view/pharmaceutical-science-new/","test_types":["K"]},
  {"name":"Pharmaceutics (New)","url":"/products/product-catalog/view/pharmaceutics-new/","test_types":["K"]},
  {"name":"Pharmacology (New)","url":"/products/product-catalog/view/pharmacology-new/","test_types":["K"]},
  {"name":"PHP (New)","url":"/products/product-catalog/view/php-new/","test_types":["K"]},
  {"name":"PJM Development Report","url":"/products/product-catalog/view/pjm-development-report/","test_types":["C","A","P"]},
  {"name":"PJM Selection Report","url":"/products/product-catalog/view/pjm-selection-report/","test_types":["A","C","P"]},
  {"name":"Polymer Engineering (New)","url":"/products/product-catalog/view/polymer-engineering-new/","test_types":["K"]},
  {"name":"Power Electronics and Drives (New)","url":"/products/product-catalog/view/power-electronics-and-drives-new/","test_types":["K"]},
  {"name":"Power System Engineering (New)","url":"/products/product-catalog/view/power-system-engineering-new/","test_types":["K"]},
  {"name":"Prism (New)","url":"/products/product-catalog/view/prism-new/","test_types":["K"]},
  {"name":"Production and Industrial Engineering (New)","url":"/products/product-catalog/view/production-and-industrial-engineering-new/","test_types":["K"]},
  # Page 22 (start=264)
  {"name":"Production Engineering (New)","url":"/products/product-catalog/view/production-engineering-new/","test_types":["K"]},
  {"name":"Programming Concepts","url":"/products/product-catalog/view/programming-concepts/","test_types":["K"]},
  {"name":"Project Management (2013)","url":"/products/product-catalog/view/project-management-2013/","test_types":["K"]},
  {"name":"Proofreading v1","url":"/products/product-catalog/view/proofreading-v1/","test_types":["K"]},
  {"name":"Python (New)","url":"/products/product-catalog/view/python-new/","test_types":["K"]},
  {"name":"R Programming (New)","url":"/products/product-catalog/view/r-programming-new/","test_types":["K"]},
  {"name":"ReactJS (New)","url":"/products/product-catalog/view/reactjs-new/","test_types":["K"]},
  {"name":"Reading Comprehension - English v1","url":"/products/product-catalog/view/reading-comprehension-english-v1/","test_types":["A"]},
  {"name":"Reading Comprehension - Spanish v1","url":"/products/product-catalog/view/reading-comprehension-spanish-v1/","test_types":["A"]},
  {"name":"Reading Comprehension v2","url":"/products/product-catalog/view/reading-comprehension-v2/","test_types":["A"]},
  {"name":"RemoteWorkQ","url":"/products/product-catalog/view/remoteworkq/","test_types":["C"]},
  {"name":"RemoteWorkQ Manager Report","url":"/products/product-catalog/view/remoteworkq-manager-report/","test_types":["C"]},
  # Page 23 (start=276)
  {"name":"RemoteWorkQ Participant Report","url":"/products/product-catalog/view/remoteworkq-participant-report/","test_types":["C"]},
  {"name":"RESTful Web Services (New)","url":"/products/product-catalog/view/restful-web-services-new/","test_types":["K"]},
  {"name":"Retail Sales and Service Simulation","url":"/products/product-catalog/view/retail-sales-and-service-simulation/","test_types":["B","K","S","A"]},
  {"name":"Reviewing Forms - US (R1)","url":"/products/product-catalog/view/reviewing-forms-us-r1/","test_types":["K"]},
  {"name":"Ruby (New)","url":"/products/product-catalog/view/ruby-new/","test_types":["K"]},
  {"name":"Ruby on Rails (New)","url":"/products/product-catalog/view/ruby-on-rails-new/","test_types":["K"]},
  {"name":"Sales & Service Phone Simulation","url":"/products/product-catalog/view/sales-and-service-phone-simulation/","test_types":["S","B"]},
  {"name":"Sales & Service Phone Solution","url":"/products/product-catalog/view/sales-and-service-phone-solution/","test_types":["B","P","S"]},
  {"name":"Sales Interview Guide","url":"/products/product-catalog/view/sales-interview-guide/","test_types":["P"]},
  {"name":"Sales Profiler Cards","url":"/products/product-catalog/view/sales-profiler-cards/","test_types":["P"]},
  {"name":"Sales Transformation 1.0 - Individual Contributor","url":"/products/product-catalog/view/sales-transformation-report-individual-contributor/","test_types":["P"]},
  {"name":"Sales Transformation 2.0 - Individual Contributor","url":"/products/product-catalog/view/salestransformationreport2-0-individualcontributor/","test_types":["P"]},
  # Page 24 (start=288)
  {"name":"Sales Transformation Report 1.0 - Sales Manager","url":"/products/product-catalog/view/sales-transformation-report-sales-manager/","test_types":["P"]},
  {"name":"Sales Transformation Report 2.0 - Sales Manager","url":"/products/product-catalog/view/sales-transformation-report-2-0-sales-manager/","test_types":["P"]},
  {"name":"Salesforce Development (New)","url":"/products/product-catalog/view/salesforce-development-new/","test_types":["K"]},
  {"name":"SAP ABAP (Advanced Level) (New)","url":"/products/product-catalog/view/sap-abap-advanced-level-new/","test_types":["K"]},
  {"name":"SAP ABAP (Intermediate Level) (New)","url":"/products/product-catalog/view/sap-abap-intermediate-level-new/","test_types":["K"]},
  {"name":"SAP Basis (New)","url":"/products/product-catalog/view/sap-basis-new/","test_types":["K"]},
  {"name":"SAP Business Objects WebI (New)","url":"/products/product-catalog/view/sap-business-objects-webi-new/","test_types":["K"]},
  {"name":"SAP BW (Business Warehouse) (New)","url":"/products/product-catalog/view/sap-bw-business-warehouse-new/","test_types":["K"]},
  {"name":"SAP HCM (Human Capital Management) (New)","url":"/products/product-catalog/view/sap-hcm-human-capital-management-new/","test_types":["K"]},
  {"name":"SAP Hybris (New)","url":"/products/product-catalog/view/sap-hybris-new/","test_types":["K"]},
  {"name":"SAP Materials Management (New)","url":"/products/product-catalog/view/sap-materials-management-new/","test_types":["K"]},
  {"name":"SAP SD (Sales and Distribution) (New)","url":"/products/product-catalog/view/sap-sd-sales-and-distribution-new/","test_types":["K"]},
  # Page 25 (start=300)
  {"name":"Search Engine Optimization (New)","url":"/products/product-catalog/view/search-engine-optimization-new/","test_types":["K"]},
  {"name":"Selenium (New)","url":"/products/product-catalog/view/selenium-new/","test_types":["K"]},
  {"name":"Shell Scripting (New)","url":"/products/product-catalog/view/shell-scripting-new/","test_types":["K"]},
  {"name":"SHL Verify Interactive - Inductive Reasoning","url":"/products/product-catalog/view/shl-verify-interactive-inductive-reasoning/","test_types":["A","S"]},
  {"name":"SHL Verify Interactive – Deductive Reasoning","url":"/products/product-catalog/view/shl-verify-interactive-deductive-reasoning/","test_types":["A","S"]},
  {"name":"SHL Verify Interactive – Numerical Reasoning","url":"/products/product-catalog/view/shl-verify-interactive-numerical-reasoning/","test_types":["A","S"]},
  {"name":"SHL Verify Interactive G+","url":"/products/product-catalog/view/shl-verify-interactive-g/","test_types":["A"]},
  {"name":"SHL Verify Interactive Numerical Calculation","url":"/products/product-catalog/view/shl-verify-interactive-numerical-calculation/","test_types":["A"]},
  {"name":"Siebel Development (New)","url":"/products/product-catalog/view/siebel-development-new/","test_types":["K"]},
  {"name":"Smart Interview Live","url":"/products/product-catalog/view/smart-interview-live/","test_types":["P"]},
  {"name":"Smart Interview Live Coding","url":"/products/product-catalog/view/smart-interview-live-coding/","test_types":["K"]},
  {"name":"Smart Interview On Demand","url":"/products/product-catalog/view/smart-interview-on-demand/","test_types":["P"]},
  # Page 26 (start=312)
  {"name":"Social Media (New)","url":"/products/product-catalog/view/social-media-new/","test_types":["K"]},
  {"name":"Software Business Analysis","url":"/products/product-catalog/view/software-business-analysis/","test_types":["K"]},
  {"name":"SonarQube (New)","url":"/products/product-catalog/view/sonarqube-new/","test_types":["K"]},
  {"name":"Spelling (U.S.) (New)","url":"/products/product-catalog/view/spelling-u-s-new/","test_types":["K"]},
  {"name":"Split Screen Typing Test - Form 1","url":"/products/product-catalog/view/split-screen-typing-test-form-1/","test_types":["A","K"]},
  {"name":"Spring (New)","url":"/products/product-catalog/view/spring-new/","test_types":["K"]},
  {"name":"SQL (New)","url":"/products/product-catalog/view/sql-new/","test_types":["K"]},
  {"name":"SQL Server (New)","url":"/products/product-catalog/view/sql-server-new/","test_types":["K"]},
  {"name":"SQL Server Analysis Services (SSAS) (New)","url":"/products/product-catalog/view/sql-server-analysis-services-%28ssas%29-%28new%29/","test_types":["K"]},
  {"name":"SQL Server Integration Services (SSIS) (New)","url":"/products/product-catalog/view/sql-server-integration-services-ssis-new/","test_types":["K"]},
  {"name":"SQL Server Reporting Services (SSRS) (New)","url":"/products/product-catalog/view/sql-server-reporting-services-ssrs-new/","test_types":["K"]},
  {"name":"Statistical Analysis System (New)","url":"/products/product-catalog/view/statistical-analysis-system-new/","test_types":["K"]},
  # Page 27 (start=324)
  {"name":"Struts (New)","url":"/products/product-catalog/view/struts-new/","test_types":["K"]},
  {"name":"SVAR - Spoken English (AUS)","url":"/products/product-catalog/view/svar-spoken-english-aus/","test_types":["S"]},
  {"name":"SVAR - Spoken English (Indian Accent) (New)","url":"/products/product-catalog/view/svar-spoken-english-indian-accent-new/","test_types":["S"]},
  {"name":"SVAR - Spoken English (U.K.)","url":"/products/product-catalog/view/svar-spoken-english-u-k/","test_types":["S"]},
  {"name":"SVAR - Spoken English (US) (New)","url":"/products/product-catalog/view/svar-spoken-english-us-new/","test_types":["S"]},
  {"name":"SVAR - Spoken French (Canadian) (New)","url":"/products/product-catalog/view/svar-spoken-french-canadian-new/","test_types":["S"]},
  {"name":"SVAR - Spoken French (European) (New)","url":"/products/product-catalog/view/svar-spoken-french-european-new/","test_types":["S"]},
  {"name":"SVAR - Spoken Spanish (Castilian) (New)","url":"/products/product-catalog/view/svar-spoken-spanish-castilian-new/","test_types":["S"]},
  {"name":"SVAR - Spoken Spanish (North American) (New)","url":"/products/product-catalog/view/svar-spoken-spanish-north-american-new/","test_types":["S"]},
  {"name":"Swing (New)","url":"/products/product-catalog/view/swing-new/","test_types":["K"]},
  {"name":"Tableau (New)","url":"/products/product-catalog/view/tableau-new/","test_types":["K"]},
  {"name":"Telecommunications Engineering (New)","url":"/products/product-catalog/view/telecommunications-engineering-new/","test_types":["K"]},
  # Page 28 (start=336)
  {"name":"Teradata Development (New)","url":"/products/product-catalog/view/teradata-development-new/","test_types":["K"]},
  {"name":"Time Management (U.S.)","url":"/products/product-catalog/view/time-management-u-s/","test_types":["K"]},
  {"name":"Training Development","url":"/products/product-catalog/view/training-development/","test_types":["K"]},
  {"name":"Typing (New)","url":"/products/product-catalog/view/typing-new/","test_types":["S"]},
  {"name":"UiPath RPA Development (New)","url":"/products/product-catalog/view/uipath-rpa-development-new/","test_types":["K"]},
  {"name":"Universal Competency Framework Interview Guide","url":"/products/product-catalog/view/universal-competency-framework-interview-guide/","test_types":["C","P"]},
  {"name":"Universal Competency Framework Job profiling guide","url":"/products/product-catalog/view/universal-competency-framework-job-profiling-guide/","test_types":["C","P"]},
  {"name":"Universal Competency Framework Profiler Cards (44)","url":"/products/product-catalog/view/universal-competency-framework-profiler-cards-44/","test_types":["C","P"]},
  {"name":"UNIX (New)","url":"/products/product-catalog/view/unix-new/","test_types":["K"]},
  {"name":"VB.NET (New)","url":"/products/product-catalog/view/vb-net-new/","test_types":["K"]},
  {"name":"Verify - Deductive Reasoning","url":"/products/product-catalog/view/verify-deductive-reasoning/","test_types":["A"]},
  {"name":"Verify - Following Instructions","url":"/products/product-catalog/view/verify-following-instructions/","test_types":["A"]},
  # Page 29 (start=348)
  {"name":"Verify - G+","url":"/products/product-catalog/view/verify-g/","test_types":["A"]},
  {"name":"Verify - General Ability Screen","url":"/products/product-catalog/view/verify-general-ability-screen/","test_types":["A"]},
  {"name":"Verify - Inductive Reasoning (2014)","url":"/products/product-catalog/view/verify-inductive-reasoning-2014/","test_types":["A"]},
  {"name":"Verify - Numerical Ability","url":"/products/product-catalog/view/verify-numerical-ability/","test_types":["A"]},
  {"name":"Verify - Technical Checking - Next Generation","url":"/products/product-catalog/view/verify-technical-checking-next-generation/","test_types":["A"]},
  {"name":"Verify - Verbal Ability - Next Generation","url":"/products/product-catalog/view/verify-verbal-ability-next-generation/","test_types":["A"]},
  {"name":"Verify - Working with Information","url":"/products/product-catalog/view/verify-working-with-information/","test_types":["A"]},
  {"name":"Verify G+ - Ability Test Report","url":"/products/product-catalog/view/verify-g-ability-test-report/","test_types":["A"]},
  {"name":"Verify G+ - Candidate Report","url":"/products/product-catalog/view/verify-g-candidate-report/","test_types":["A"]},
  {"name":"Verify Interactive Ability Report","url":"/products/product-catalog/view/verify-interactive-ability-report/","test_types":["A"]},
  {"name":"Verify Interactive G+ Candidate Report","url":"/products/product-catalog/view/verify-interactive-g-candidate-report/","test_types":["A"]},
  {"name":"Verify Interactive G+ Report","url":"/products/product-catalog/view/verify-interactive-g-report/","test_types":["A"]},
  # Page 30 (start=360)
  {"name":"Verify Interactive Process Monitoring","url":"/products/product-catalog/view/verify-interactive-process-monitoring/","test_types":["A"]},
  {"name":"Virtual Assessment and Development Centers","url":"/products/product-catalog/view/virtual-assessment-and-development-centers/","test_types":["P"]},
  {"name":"Visual Basic for Applications (New)","url":"/products/product-catalog/view/visual-basic-for-applications-new/","test_types":["K"]},
  {"name":"Visual Comparison - UK","url":"/products/product-catalog/view/visual-comparison-uk/","test_types":["K"]},
  {"name":"Visual Comparison - US","url":"/products/product-catalog/view/visual-comparison-us/","test_types":["K"]},
  {"name":"VLSI and Embedded Systems (New)","url":"/products/product-catalog/view/vlsi-and-embedded-systems-new/","test_types":["K"]},
  {"name":"What Is The Value - US","url":"/products/product-catalog/view/what-is-the-value-us/","test_types":["K"]},
  {"name":"Workplace Administration Skills (New)","url":"/products/product-catalog/view/workplace-administration-skills-new/","test_types":["K"]},
  {"name":"Workplace Health and Safety (New)","url":"/products/product-catalog/view/workplace-health-and-safety-new/","test_types":["K"]},
  {"name":"WriteX - Email Writing (Customer Service) (New)","url":"/products/product-catalog/view/writex-email-writing-customer-service-new/","test_types":["S"]},
  {"name":"WriteX - Email Writing (Managerial) (New)","url":"/products/product-catalog/view/writex-email-writing-managerial-new/","test_types":["S"]},
  {"name":"WriteX - Email Writing (Sales) (New)","url":"/products/product-catalog/view/writex-email-writing-sales-new/","test_types":["B","S"]},
  # Page 31 (start=372)
  {"name":"Written English v1","url":"/products/product-catalog/view/written-english-v1/","test_types":["K"]},
  {"name":"Written Spanish","url":"/products/product-catalog/view/written-spanish/","test_types":["K"]},
  {"name":"Zabbix (New)","url":"/products/product-catalog/view/zabbix-new/","test_types":["K"]},
  {"name":"360 Digital Report","url":"/products/product-catalog/view/360-digital-report/","test_types":["D"]},
  {"name":"360° Multi-Rater Feedback System (MFS)","url":"/products/product-catalog/view/360-multi-rater-feedback-system-mfs/","test_types":["D","P"]},
]

# Enriched descriptions for key assessments
DESCRIPTIONS = {
  "Occupational Personality Questionnaire OPQ32r": (
    "Measures 32 personality dimensions relevant to workplace behavior including thinking style, "
    "relationships with people, feelings and emotions, and dynamism. The gold standard for personality "
    "assessment in selection, development, and succession planning. Suitable for all professional levels."
  ),
  "Motivation Questionnaire MQM5": (
    "Assesses 18 factors that motivate or de-motivate individuals at work. Helps predict engagement, "
    "fit with role and culture, and retention risk. Used in selection, onboarding, and career development."
  ),
  "SHL Verify Interactive G+": (
    "Adaptive general cognitive ability test combining numerical, verbal, and deductive reasoning. "
    "Measures overall mental capability — the strongest single predictor of job performance. "
    "Adaptive format adjusts to candidate ability level for greater precision."
  ),
  "SHL Verify Interactive – Numerical Reasoning": (
    "Assesses ability to analyze and interpret numerical data in tables and charts. "
    "Critical for roles requiring financial analysis, data interpretation, or quantitative decision-making. "
    "Interactive simulation format improves candidate experience."
  ),
  "SHL Verify Interactive – Deductive Reasoning": (
    "Measures ability to draw logical conclusions from given information and scenarios. "
    "Evaluates analytical and logical thinking essential for managers, analysts, and professional roles."
  ),
  "SHL Verify Interactive - Inductive Reasoning": (
    "Assesses ability to identify patterns and rules from abstract visual information. "
    "Measures fluid intelligence and problem-solving capability. Strong predictor of learning agility."
  ),
  "SHL Verify Interactive Numerical Calculation": (
    "Assesses basic numerical calculation ability including arithmetic operations. "
    "Used for roles requiring accurate numeracy such as finance, retail, and administrative positions."
  ),
  "Verify - G+": (
    "General cognitive ability test measuring numerical, verbal, and deductive reasoning combined. "
    "Single strongest predictor of job performance across all roles and levels."
  ),
  "Verify - Numerical Ability": (
    "Assesses ability to work with numerical data and perform quantitative analysis. "
    "Used for roles requiring strong numerical reasoning and data interpretation."
  ),
  "Verify - Deductive Reasoning": (
    "Measures logical reasoning and ability to draw conclusions from given information. "
    "Suitable for analytical, managerial, and professional roles."
  ),
  "Verify - Inductive Reasoning (2014)": (
    "Measures ability to identify patterns in abstract information. Predicts learning agility "
    "and problem-solving. Used across all levels from graduate to senior management."
  ),
  "Verify - Verbal Ability - Next Generation": (
    "Assesses verbal reasoning, comprehension, and language ability. "
    "Used for roles requiring strong communication, analysis, and written expression skills."
  ),
  "Verify - Technical Checking - Next Generation": (
    "Measures attention to detail and accuracy in checking numerical and textual information. "
    "Ideal for administrative, finance, data entry, and quality control roles."
  ),
  "Verify - Working with Information": (
    "Assesses ability to analyze and interpret a combination of numerical and verbal information. "
    "Suitable for roles requiring broad analytical and critical thinking skills."
  ),
  "Verify - General Ability Screen": (
    "Short screening assessment of general cognitive ability combining verbal and numerical elements. "
    "Efficient screener for high-volume hiring at entry and mid-level."
  ),
  "Verify - Following Instructions": (
    "Measures ability to understand and follow complex written and numerical instructions accurately. "
    "Key for administrative, operational, and compliance-oriented roles."
  ),
  "Graduate Scenarios": (
    "Situational judgement test for graduate and entry-level candidates. Presents realistic workplace "
    "scenarios and asks candidates to identify the most effective responses. Measures professional "
    "judgment, teamwork, communication, and business awareness."
  ),
  "Management Scenarios": (
    "Situational judgement test for experienced managers and team leaders. Assesses management "
    "judgment in challenging situations including people management, stakeholder influence, "
    "performance management, and conflict resolution."
  ),
  "Executive Scenarios": (
    "Situational judgement test for senior leaders and C-suite executives. Evaluates strategic "
    "thinking, organizational decision-making, leadership under pressure, and executive judgment."
  ),
  "Global Skills Assessment": (
    "Comprehensive skills assessment measuring competency across SHL's Great 8 domains: Leading, "
    "Supporting, Presenting, Analyzing, Creating, Organizing, Adapting, and Enterprising. "
    "Provides a 360-degree skills profile for individuals and teams."
  ),
  "Global Skills Development Report": (
    "Delivered after completing the Global Skills Assessment. Provides a complete overview of "
    "skill strengths and development areas across the Great 8 domains with actionable development "
    "recommendations. Includes reskilling-focused variant."
  ),
  "AI Skills": (
    "Measures individual attitudes, confidence, and behavioral tendencies toward AI tools and "
    "digital transformation. Identifies AI-ready talent, growth mindset, and adaptability. "
    "Relevant for all roles in digitally transforming organizations."
  ),
  "Assessment and Development Center Exercises": (
    "A range of structured assessment center exercises including in-tray/e-tray, group discussions, "
    "presentations, role plays, and written analyses. Used for selection, promotion, and development "
    "assessment centers across management levels."
  ),
  "Virtual Assessment and Development Centers": (
    "Digital assessment center platform enabling organizations to run online assessment and "
    "development centers. Includes exercises for evaluating leadership, judgment, and competencies "
    "in a virtual format suitable for remote hiring."
  ),
  "Dependability and Safety Instrument (DSI)": (
    "Measures safety awareness, reliability, conscientiousness, and dependability. Designed for "
    "roles where safety is critical including manufacturing, healthcare, transportation, and "
    "utilities. Predicts safe working behaviors and reliability."
  ),
  "DSI v1.1 Interpretation Report": (
    "Detailed interpretation report for the Dependability and Safety Instrument. Provides "
    "behavioral insights on safety, reliability, and dependability for hiring decisions "
    "in safety-critical roles."
  ),
  "RemoteWorkQ": (
    "Assesses readiness and effectiveness for remote and hybrid work. Measures key competencies "
    "for distributed work: self-management, communication, digital collaboration, resilience, "
    "and results orientation."
  ),
  "HiPo Assessment Report 1.0": (
    "Identifies high-potential employees across multiple dimensions including learning agility, "
    "leadership capability, aspiration, and engagement. Used for talent identification, "
    "succession planning, and accelerated development programs."
  ),
  "HiPo Assessment Report 2.0": (
    "Updated version identifying high-potential talent. Assesses potential across learning agility, "
    "leadership readiness, and career aspirations. Used in talent reviews and succession planning."
  ),
  "OPQ Leadership Report": (
    "Derived from OPQ32r personality data. Focuses on leadership potential across key competency "
    "areas: achieving goals, supporting others, and creating change. Used for leadership selection "
    "and development at all levels."
  ),
  "OPQ Emotional Intelligence Report": (
    "Uses OPQ32r data to assess emotional intelligence competencies: self-awareness, self-management, "
    "empathy, and relationship management. Useful for leadership development and coaching."
  ),
  "OPQ Manager Plus Report": (
    "Comprehensive report from OPQ32r for managerial selection and development. Covers management "
    "style, leadership behaviors, and fit for management roles."
  ),
  "OPQ Manager Plus Report 2.0": (
    "Updated managerial OPQ report providing deeper insight into management competencies and "
    "behavioral tendencies. Used for mid-level and senior manager selection."
  ),
  "OPQ Universal Competency Report 1.0": (
    "Maps OPQ32r personality data to the Universal Competency Framework (UCF). Provides "
    "competency predictions for 20 key workplace competencies used in selection and development."
  ),
  "OPQ Universal Competency Report 2.0": (
    "Enhanced version mapping OPQ32r to the Universal Competency Framework. Provides updated "
    "competency predictions with improved narratives for 20 key workplace competencies."
  ),
  "OPQ MQ Sales Report": (
    "Combines OPQ32r personality and MQ motivation data to assess sales effectiveness. "
    "Predicts performance across key sales competencies including prospecting, influencing, "
    "and closing. Designed for sales role selection and development."
  ),
  "Enterprise Leadership Report 1.0": (
    "Derived from OPQ32r. Provides a comprehensive view of enterprise leadership capability "
    "for senior executive selection and development."
  ),
  "Enterprise Leadership Report 2.0": (
    "Updated enterprise leadership report with enhanced competency coverage for C-suite and "
    "senior executive assessment."
  ),
  "PJM Selection Report": (
    "Project Manager assessment combining ability, competency, and personality measures. "
    "Evaluates project management capability, analytical thinking, and professional judgment "
    "for PM selection at various experience levels."
  ),
  "PJM Development Report": (
    "Development-focused project manager assessment providing insight into PM competencies, "
    "development areas, and coaching recommendations."
  ),
  "Retail Sales and Service Simulation": (
    "Simulation of retail customer interactions assessing sales ability, customer service, "
    "problem-solving, and interpersonal effectiveness. Used for retail and sales role selection."
  ),
  "Customer Service Phone Simulation": (
    "Simulates real customer service phone interactions. Assesses call handling, problem resolution, "
    "empathy, and communication skills. Used for contact center and customer service hiring."
  ),
  "Customer Service Phone Solution": (
    "Comprehensive assessment for customer service phone roles combining personality, situational "
    "judgement, and simulation. Predicts customer service performance and satisfaction."
  ),
  "Manufacturing & Industrial - Essential Focus 8.0": (
    "Job-focused personality and behavioral assessment for manufacturing and industrial workers. "
    "Measures essential work attitudes including reliability, teamwork, and safety consciousness."
  ),
  "Manufac. & Indust. - Mechanical & Vigilance 8.0": (
    "Assesses mechanical aptitude and attention to detail for manufacturing and industrial roles "
    "requiring both mechanical understanding and sustained vigilance."
  ),
  "Manufac. & Indust. - Safety & Dependability 8.0": (
    "Focused assessment measuring safety awareness and dependability for high-safety manufacturing "
    "and industrial environments."
  ),
  "Manufacturing & Industrial - Mechanical Focus 8.0": (
    "Assesses mechanical reasoning and aptitude for manufacturing, maintenance, and engineering roles."
  ),
  "Manufacturing & Industrial - Vigilance Focus 8.0": (
    "Measures sustained attention and vigilance for roles requiring monitoring of equipment, "
    "processes, or quality control in manufacturing settings."
  ),
  "Smart Interview Live": (
    "Structured live video interview platform enabling standardized behavioral and competency-based "
    "interviewing. Supports scoring against predefined competency frameworks with built-in interview guides."
  ),
  "Smart Interview On Demand": (
    "Asynchronous one-way video interview tool. Candidates record responses to preset questions "
    "at their convenience for later review by hiring managers. Used for high-volume screening."
  ),
  "Smart Interview Live Coding": (
    "Technical live interview with integrated coding environment. Candidates solve coding challenges "
    "in real-time while interviewers observe. Used for software developer and technical role screening."
  ),
  "Automata (New)": (
    "Live coding simulation platform for software developers. Candidates write and run code in a "
    "realistic IDE environment. Assesses coding ability, algorithmic thinking, and software "
    "development problem-solving skills."
  ),
  "Automata Pro (New)": (
    "Advanced live coding assessment for experienced developers. Supports complex coding challenges "
    "across multiple programming languages. Used for senior developer and architect selection."
  ),
  "Automata - Fix (New)": (
    "Code debugging simulation where candidates fix broken code. Assesses debugging ability, "
    "code comprehension, and problem-solving for software engineering roles."
  ),
  "Automata - SQL (New)": (
    "SQL coding simulation where candidates write and execute SQL queries against a real database. "
    "Assesses SQL proficiency for data analyst, database developer, and backend engineer roles."
  ),
  "Automata Data Science (New)": (
    "Data science coding simulation assessing Python/R programming, data manipulation, and "
    "statistical analysis. Used for data scientist and data analyst role selection."
  ),
  "Automata Front End": (
    "Front-end coding simulation assessing HTML, CSS, and JavaScript skills in a browser-based "
    "environment. Used for front-end developer and UI engineer selection."
  ),
  "MFS 360 UCF Standard Report": (
    "360-degree multi-rater feedback report mapped to the Universal Competency Framework. "
    "Provides structured feedback from managers, peers, and direct reports on key competencies."
  ),
  "360 Digital Report": (
    "Digital 360-degree feedback report for leadership development. Collects multi-rater input "
    "on leadership behaviors and provides development recommendations."
  ),
  "360° Multi-Rater Feedback System (MFS)": (
    "Comprehensive 360-degree multi-rater feedback platform. Captures behavioral feedback from "
    "multiple stakeholders for leadership development and performance management."
  ),
  "Digital Readiness Development Report - IC": (
    "Assesses individual contributor readiness for digital transformation and AI adoption. "
    "Measures digital confidence, adaptability, and growth mindset."
  ),
  "Digital Readiness Development Report - Manager": (
    "Assesses manager readiness to lead digital transformation. Measures digital leadership "
    "capability, team enablement, and change management for the digital era."
  ),
  "Sales Transformation 1.0 - Individual Contributor": (
    "Measures sales effectiveness for individual contributors across modern B2B selling. "
    "Covers consultative selling, digital sales, and relationship management competencies."
  ),
  "Sales Transformation 2.0 - Individual Contributor": (
    "Updated sales assessment for individual contributors emphasizing consultative, value-based, "
    "and digital selling skills for modern sales environments."
  ),
  "Sales Transformation Report 1.0 - Sales Manager": (
    "Assesses sales management capability including coaching, pipeline management, and "
    "sales team leadership. For hiring and developing sales managers."
  ),
  "OPQ Team Impact Selection Report": (
    "Uses OPQ32r data to predict team contribution and fit. Assesses eight team types and "
    "leadership styles for team composition and selection decisions."
  ),
  "Multitasking Ability": (
    "Assesses ability to manage multiple tasks simultaneously while maintaining accuracy. "
    "Used for roles requiring high cognitive load management such as dispatchers, coordinators, "
    "and contact center agents."
  ),
  "Verify Interactive Process Monitoring": (
    "Assesses sustained attention and vigilance while monitoring automated process information. "
    "Used for process control, operations, and monitoring roles in industrial settings."
  ),
  "Entry Level Sales Solution": (
    "Combines personality and competency assessments for entry-level sales hiring. "
    "Predicts sales aptitude, customer orientation, and resilience."
  ),
  "Entry Level Customer Service (General) Solution": (
    "Combines personality and competency measures for customer service role selection. "
    "Assesses service orientation, communication, and problem-solving."
  ),
  "Entry Level Technical Support Solution": (
    "Assesses technical aptitude, customer service skills, and problem-solving for "
    "entry-level IT support and helpdesk roles."
  ),
  "Contact Center Call Simulation (New)": (
    "Simulates contact center call interactions for selection of customer service and sales agents. "
    "Assesses call handling, empathy, and resolution skills in a realistic environment."
  ),
}


def build_catalog() -> list[dict]:
    catalog = []
    seen_urls = set()

    for item in RAW_ITEMS:
        url_path = item.get("url") or item.get("url_path", "")
        if not url_path:
            continue
        full_url = BASE_URL + url_path if url_path.startswith("/") else url_path

        if full_url in seen_urls:
            continue
        seen_urls.add(full_url)

        entry = {
            "name": item["name"],
            "url": full_url,
            "test_types": item["test_types"],
            "description": DESCRIPTIONS.get(item["name"]),
        }
        catalog.append(entry)

    return catalog


if __name__ == "__main__":
    catalog = build_catalog()
    output = Path(__file__).parent / "catalog.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"Written {len(catalog)} items to {output}")
