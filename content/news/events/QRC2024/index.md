---
# Documentation: https://docs.hugoblox.com/managing-content/
type: event
title: 
  
subtitle: 
summary: |
  <h2><p style="text-align: center;color:#3366CC"><a href="events/qrc2024">Working Party on Quantum Reservoir Computing</a></p></h2>
  <h2><p style="text-align: center;">15/18 October 2024</p></h2>

tags: []
categories: []
date: 2024-5-14
#date_end: 2024-10-18

# Optional external URL for project (replaces project detail page).
#external_link: ""

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
#image:
#  caption: ""
#  focal_point: ""
#  preview_only: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

#url_code: 
#url_pdf: 
#url_slides: 
#url_video: 

# Slides (optional).
#   Associate this project with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
#slides: ""
#authors: [salvatore-lorenzo, g.-massimo-palma, mauro-paternostro]
---
<html lang="en">


<title></title>
    <style>
        .myButton {
            background-color: blue; /* Background color */
            color: white;           /* Text color */
            border: none;           /* Remove borders if needed */
            padding: 10px 20px;
            border-radius: 5px;     /* Optional rounded corners */
        }
        /* Hover effect */
        .myButton:hover {
          background-color: darkblue;
        }
        .nav-link[data-bs-target]:hover {
        }
        .nav-link[data-bs-target] {
            color: black;
            background-color: #f0f0f0;
            border-color: var(--bs-btn-hover-border-color);
        }
        .nav-link[data-bs-target].active {
            color: #FFFFFF;
            background-color: #7799AA;
            border-color: var(--bs-btn-hover-border-color);
        }
        .event-row {
            display: flex;
            align-items: stretch;
            margin-bottom: 0px;
            /*border: 2px solid white;*/
        }
        .event-time {
            width: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            /*padding: 0px;*/
        }
        .event-description {
            flex-grow: 2;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
            padding: 0px 20px 20px 20px;
        }
        .event-description-break {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
            padding: 0px 0px 0px 0px;
        }
        .speaker-name {
            cursor: pointer;
            color: #3366CC;
            text-decoration: underline;
        }
        .speaker-name:hover {
            color: #0056b3;
        }
        .blue-bg {
            background-color: #3366CC;
            color: white;
        }
        .gray-bg {
            background-color: #7799AA;
            color: white;
        }
        .light-gray-bg {
            background-color: #f0f0f0;
        }
        .white-bg {
            background-color: #ffffff;
        }
        .dark-gray-bg {
            background-color: rgb(220,220,220);
        }
        .program-container {
            height: 800px; /* Adjust this value to change the overall height of the schedule */
        }
    </style>


<body>

<div class="container my-5">
        <header class="text-center mb-5">
            <h1>QRC2024</h1>
            <p class="small">This Course is hosted at the</p>
            <h4>ETTORE MAJORANA FOUNDATION AND CENTRE FOR SCIENTIFIC CULTURE</h4>
            <p class="small">DIRECTOR: A. ZICHICHI</p>
            <p class="small">as part of the</p>
            <h2>INTERNATIONAL SCHOOL ON NONEQUILIBRIUM PHENOMENA</h2>
            <p>Directors of the School: A. Lanzara, G. M. Palma, B. Spagnolo</p>
            <h2 class="text-primary">Working Party on Quantum Reservoir Computing</h2>
            <p>Directors of the Course: S. Lorenzo, G. M. Palma, M. Paternostro</p>
            <p>Dates: 15 - 18 October 2024</p>
        </header>
        <section class="mb-5">
            <p>
                The aim of the course is to discuss the current understanding of quantum reservoir computing and to develop characterization tools for tum computation and process identification. The features of specific platforms currently being explored for these goals will be considered, as well as impact of noise and thermodynamic constraints. <br> The working party will discuss the range of tasks that can be efficiently solved by QRC and, bly, the combination of analytical and numerical approaches, including the exploitation of quantum simulation on quantum computing platforms.
            </p>
            <p>If you want to join us, please <a href="https://docs.google.com/forms/d/16PHgeI1JZ3a76JzZBJH7RkPYNi6iKZcnkFfdmD1T6Bw/edit?6f3e6eb#response=ACYDBNjvW-b0BZf63AWMP9sBHFWIgcsYo5Gsa-BvJ0S21nzUB6mktHnY1RX4NluflDVXMc">REGISTER</a>.</p>
        </section>
        <section>
            <h2 class="text-center mb-4">Program</h2>
            <ul class="nav nav-pills mb-3 justify-content-center" id="myTab" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="d1-tab" data-bs-toggle="tab" data-bs-target="#day1" type="button" role="tab" -controls="day1" aria-selected="true">Day 1 (Oct 15)</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="d2-tab" data-bs-toggle="tab" data-bs-target="#day2" type="button" role="tab" aria-controls="day2" -selected="false">Day 2 (Oct 16)</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="d3-tab" data-bs-toggle="tab" data-bs-target="#day3" type="button" role="tab" aria-controls="day3" -selected="false">Day 3 (Oct 17)</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="d4-tab" data-bs-toggle="tab" data-bs-target="#day4" type="button" role="tab" aria-controls="day4" -selected="false">Day 4 (Oct 18)</button>
                </li>
            </ul>

<div class="tab-content" id="myTabContent">

<!-- Day 1 -->
<div class="tab-pane fade show active" id="day1" role="tabpanel" aria-labelledby="d1-tab">
                    <div class="program-container">
                        <div class="event-row blue-bg" data-duration="60">
                            <div class="event-time">10:30 - 12:30</div>
                            <div class="event-description-break">Arrivals, opening and registration</div>
                        </div>
                        <div class="event-row gray-bg" data-duration="60">
                            <div class="event-time">12:30 - 15:00</div>
                            <div class="event-description-break">Lunch</div>
                        </div>
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">15:00 - 15:50</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Neill">Oliver Neill</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row gray-bg" data-duration="20">
                            <div class="event-time">15:50 - 16:20</div>
                            <div class="event-description-break">Coffee break</div>
                        </div>
                        <div class="event-row dark-gray-bg" data-duration="60">
                            <div class="event-time">16:20 - 17:10</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Pezzutto">Marco Pezzutto</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">17:10 - 18:00</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Plastina">Francesco Plastina</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row white-bg" data-duration="120">
                            <div class="event-time"></div>
                            <div class="event-description" style="color:white"></div>
                        </div>
                    </div>
                </div>

<!-- Day 2 -->
<div class="tab-pane fade" id="day2" role="tabpanel" aria-labelledby="d2-tab">
                    <div class="program-container">
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">9:00 - 9:50</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Cimini">Valeria Cimini</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row dark-gray-bg" data-duration="60">
                            <div class="event-time">9:50 - 10:40</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Smirne">Andrea Smirne</h4>
                                <p class="mb-0 ">Quantumness in sequential measurements:coherences, correlations and quantum combs</p>
                            </div>
                        </div>
                        <div class="event-row gray-bg" data-duration="20">
                            <div class="event-time">10:40 - 11:10</div>
                            <div class="event-description-break">Coffee break</div>
                        </div>
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">11:10 - 12:00</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Romancino">Alessandro Romancino</h4>
                                <p class="mb-0 ">Entanglement Percolation in Random State Quantum Networks</p>
                            </div>
                        </div>
                        <div class="event-row gray-bg" data-duration="60">
                            <div class="event-time">12:00 - 15:00</div>
                            <div class="event-description-break"><p class="mb-0 ">Lunch</p></div>
                        </div>
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">15:00 - 15:50</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Sannia">Antonio Sannia</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row gray-bg" data-duration="20">
                            <div class="event-time">15:50 - 16:20</div>
                            <div class="event-description-break">Coffee break</div>
                        </div>
                        <div class="event-row dark-gray-bg" data-duration="60">
                            <div class="event-time">16:20 - 17:10</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Monaco">Gabriele Lo Monaco</h4>
                                <p class="mb-0 ">QELM for quantum chemistry and biological tasks</p>
                            </div>
                        </div>
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">17:10 - 18:00</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Ferraro">Alessandro Ferraro</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                    </div>
                </div>

<!-- Day 3 -->
<div class="tab-pane fade" id="day3" role="tabpanel" aria-labelledby="d3-tab">
                    <div class="program-container">
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">9:00 - 9:50</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Sgroi">Sofia Sgroi</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row dark-gray-bg" data-duration="60">
                            <div class="event-time">9:50 - 10:40</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Tamascelli">Dario Tamascelli</h4>
                                <p class="mb-0 ">Spectral Density Modulation and Universal Markovian Closure of Structured Environments</p>
                            </div>
                        </div>
                        <div class="event-row gray-bg" data-duration="20">
                            <div class="event-time">10:40 - 11:10</div>
                            <div class="event-description-break">Coffee break</div>
                        </div>
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">11:10 - 12:00</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Rattacaso">Davide Rattacaso</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row gray-bg" data-duration="60">
                            <div class="event-time">12:00 - 15:00</div>
                            <div class="event-description-break">Lunch</div>
                        </div>
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">15:00 - 15:50</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Colla">Alessandra Colla</h4>
                                <p class="mb-0 ">Thermodynamic role of general environments: from heat bath to work reservoir</p>
                            </div>
                        </div>
                        <div class="event-row gray-bg" data-duration="20">
                            <div class="event-time">15:50 - 16:20</div>
                            <div class="event-description-break">Coffee break</div>
                        </div>
                        <div class="event-row dark-gray-bg" data-duration="60">
                            <div class="event-time">16:20 - 17:10</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Agresti">Iris Agresti</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">17:10 - 18:00</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Vetrano">Marco Vetrano</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                    </div>
                </div>

<!-- Day 4 -->
<div class="tab-pane fade" id="day4" role="tabpanel" aria-labelledby="d4-tab">
                    <div class="program-container">
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">9:00 - 9:50</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Paterek">Tomasz Paterek</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row dark-gray-bg" data-duration="60">
                            <div class="event-time">9:50 - 10:40</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Innocenti">Luca Innocenti</h4>
                                <p class="mb-0 ">Connections Between QELM, QRC, and Shadow Tomography</p>
                            </div>
                        </div>
                        <div class="event-row gray-bg" data-duration="20">
                            <div class="event-time">10:40 - 11:10</div>
                            <div class="event-description-break">Coffee break</div>
                        </div>
                        <div class="event-row light-gray-bg" data-duration="60">
                            <div class="event-time">11:10 - 12:00</div>
                            <div class="event-description">
                                <h4 class="speaker-name" data-bs-toggle="modal" data-bs-target="#Prati">Enrico Prati</h4>
                                <p class="mb-0 small">QRC2024</p>
                            </div>
                        </div>
                        <div class="event-row blue-bg" data-duration="60">
                            <div class="event-time">12:00 - 15:00</div>
                            <div class="event-description-break">Closing & Lunch</div>
                        </div>
                        <div class="event-row white-bg" data-duration="160">
                            <div class="event-time"></div>
                            <div class="event-description" style="color:white"></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
</div>

<!--Modal Classes-->
<div class="modal fade" id="Neill" tabindex="-1" aria-labelledby="NeillModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="NeillModalLabel">Oliver Neill's Talk</h5>
                    <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
                </div>
                <div class="modal-body">
                    <h6>Title: </h6>
                    <p>Abstract: </p>
                </div>
            </div>
        </div>
</div>

<div class="modal fade" id="Pezzutto" tabindex="-1" aria-labelledby="pezzuttoModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="pezzuttoModalLabel">Marco Pezzutto's Talk</h5>
                    <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
                </div>
                <div class="modal-body">
                    <h6>Title: </h6>
                    <p>Abstract: </p>
                </div>
            </div>
        </div>
</div>

<div class="modal fade" id="Plastina" tabindex="-1" aria-labelledby="plastinaModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="plastinaModalLabel">Francesco Plastina's Talk</h5>
                <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Cimini" tabindex="-1" aria-labelledby="ciminiModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="ciminiModalLabel">Valeria Cimini's Talk</h5>
                <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Smirne" tabindex="-1" aria-labelledby="smirneModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="smirneModalLabel">Andrea Smirne's Talk</h5>
                <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
            </div>
            <div class="modal-body">
                <h6>Title: Quantumness in sequential measurements: coherences, correlations and quantum combs</h6>
                <p>Abstract: More than a century after the advent of quantum theory, identifying which properties and phenomena are fundamentally quantum remains a central and elusive challenge across various fields of investigation. How can we witness the role of quantum coherence in biological phenomena? Are there distinct behaviors associated with the principles of thermodynamics when we move to the microscopic realm? What quantum features guarantee advantages when quantum computational protocols are performed instead of classical ones? In this talk, I will discuss to what extent non-classicality can be linked to quantum coherences and quantum correlations when considering an open quantum system undergoing sequential measurements at different times. In particular, I will highlight the critical distinction between Markovian and non-Markovian processes in this context. While Markovian processes can be effectively addressed using standard quantum dynamical maps—establishing a direct link between non-classical statistics and quantum coherence dynamics—non-Markovian processes require a more comprehensive framework: quantum combs. After briefly explaining how quantum combs work in a simple case study, I will show how they allow to characterize in full generality those multi-time statistics that are properly quantum and to link them with a specific property of the system-environment correlations.</p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Romancino" tabindex="-1" aria-labelledby="romancinoModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="romancinoModalLabel">Alessandro Romancino's Talk</h5>
                <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
            </div>
            <div class="modal-body">
                <h6>Title: Entanglement Percolation in Random State Quantum Networks</h6>
                <p>Abstract: Quantum information shows that entanglement is a crucial resource for applications that go beyond classical capabilities. Thanks to quantum correlations, protocols such as secure quantum cryptography, dense coding, and quantum teleportation are now possible to implement on various scales. However, entanglement at a distance remains a challenging experimental endeavour. To address this issue, entanglement distribution employs different methods like quantum repeaters and entanglement distillation. Another technique, inspired by statistical physics, exploits the features of a quantum network of partially entangled states. This protocol, called entanglement percolation, uses local operations and classical communication (LOCC) and entanglement swapping to create a maximally entangled state between two arbitrary nodes in the network. This problem can be perfectly mapped onto the problem of percolation theory and can be simulated effectively with classical network theory. The classical entanglement percolation (CEP) threshold measures the initial amount of entanglement needed at the beginning to ensure the creation of the desired singlet. This approach has been shown to be, in general, suboptimal, and an improvement called quantum entanglement percolation (QEP) has been developed by first preparing the quantum network using local quantum operations only. Still, it is already known that this protocol is also not optimal, and finding it is still an open question. Different aspects of the problem have also been tackled, such as multipartite entanglement and mixed states. A deterministic protocol based on concurrence has also shown promising results. In our work we have generalized the problem by relaxing the original assumption that the initial states are fixed. By using random states and results from extreme value theory we have found out that only the average initial entanglement is important for entanglement distribution purposes and, in general, the QEP protocol can be worse than the CEP protocol in this more realistic scenario. </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Sannia" tabindex="-1" aria-labelledby="sanniaModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="sanniaModalLabel">Antonio Sannia's Talk</h5>
                <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Monaco" tabindex="-1" aria-labelledby="monacoModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="monacoModalLabel">Gabriele Lo Monaco's Talk</h5>
                <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
            </div>
            <div class="modal-body">
                <h6>Title: Quantum extreme learning machine for quantum chemistry and biological tasks</h6>
                <p>Abstract: Among the paradigms of quantum supervised machine learning, quantum reservoir computing, and specifically the quantum extreme learning machine (QELM), has emerged as some of the most promising approaches. The notable advantages of QELM lie in the simplicity of its optimization routine which require minimal resources. Classical data are encoded in the quantum state of input qubits, with the choice of encoding determining model’s expressivity. The information is distributed across a reservoir interacting with the encoding qubits through a fixed scrambling dynamics that does not require any optimization during training. The reservoir is then measured and the outcomes are collected on a classical computer for post-processing, the optimization step, involving a simple linear regression to fit the target data.<br>
                We present the first implementation of QELM on NISQ devices with applications to quantum chemistry and biological tasks of practical interest. We use QELM to reconstruct the potential energy surface of various molecules, mapping the geometry of a molecular species to its energy. Our setup outperforms classical neural networks and other quantum routines such as VQE, while minimizing quantum resource costs. It is scalable and has controlled depth, making it suitable for practical implementation on real hardware. The implementation performed on IBM Quantum platforms yielded encouraging results, with the average error close to chemical accuracy and no need for error mitigation.<br>
                In the biological domain, we employ QELM as a support vector machine for protein classification on large experimental datasets. A practical example is classifying proteins based on their interaction with angiotensin enzyme, predicting peptides with anti-hypertensive effects that could contribute to cardiovascular health. The proteins are described in terms of 40 descriptors of biological relevance, such as aromaticity or hydrophobicity, a large number of input features presenting a challenge and benchmark for the current status of QELM. This second application confirms the feasibility of QELM and manifests an interesting resistance to statistical noise and decoherence, suggesting its potential for imminent applications in industrial pharmacology.</p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Ferraro" tabindex="-1" aria-labelledby="ferraroModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="ferraroModalLabel">Alessandro Ferraro's Talk</h5>
                <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Sgroi" tabindex="-1" aria-labelledby="sgroiModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="sgroiModalLabel">Sofia Sgroi's Talk</h5>
                <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Tamascelli" tabindex="-1" aria-labelledby="tamascelliModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="tamascelliModalLabel">Dario Tamascelli's Talk</h5>
            </div>
            <div class="modal-body">
                <h6>Title: Spectral Density Modulation and Universal Markovian Closure of Structured Environments</h6>
                <p>Abstract: The combination of chain-mapping and tensor-network techniques provides a powerful tool for the numerically exact simulation of open quantum systems interacting with structured environments. However, these methods suffer from a quadratic scaling with the physical simulation time, and therefore they become challenging in the presence of multiple environments. In this talk we first illustrate how a thermo-chemical modulation of the spectral density allows replacing the original environments with equivalent, but simpler, ones. Moreover, we show how this procedure reduces the number of chains needed to model multiple environments. We then provide a derivation of the  Markovian closure construction, consisting of a small collection of damped  modes undergoing a Lindblad-type dynamics and mimicking a continuum of bath modes. We describe, in particular, how the use of the Markovian closure allows for a polynomial reduction of the time complexity of chain-mapping based algorithms when long-time dynamics are needed. </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Rattacaso" tabindex="-1" aria-labelledby="rattacasoModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="rattacasoModalLabel">Ddavide Rattacaso's Talk</h5>
                <!---<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>--->
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Colla" tabindex="-1" aria-labelledby="collaModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="collaModalLabel">Alessandra Colla's Talk</h5>
            </div>
            <div class="modal-body">
                <h6>Title: Thermodynamic role of general environments: from heat bath to work reservoir</h6>
                <p>Abstract: Environments in quantum thermodynamics usually take the role of heat baths. These baths are Markovian, weakly coupled to the system, and initialized in a thermal state. Whenever one of these properties is missing, standard quantum thermodynamics is no longer suitable to treat the thermodynamic properties of the system that result from the interaction with the environment. Using a recently proposed framework for open system quantum thermodynamics at arbitrary coupling regimes, we show that within the very same model (a Fano-Anderson Hamiltonian) the environment can take three different thermodynamic roles: a standard heat bath, exchanging only heat with the system, a work reservoir, exchanging only work, and a hybrid environment, providing both types of energy exchange. The exact role of the environment is determined by the strength and structure of the coupling, and by its initial state.</p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Agresti" tabindex="-1" aria-labelledby="agrestiModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="agrestiModalLabel">Iris Agresti's Talk</h5>
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Vetrano" tabindex="-1" aria-labelledby="vetranoModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="vetranoModalLabel">Marco Vetrano's Talk</h5>
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Paterek" tabindex="-1" aria-labelledby="paterekModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="paterekModalLabel">Tomasz Paterek's Talk</h5>
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Innocenti" tabindex="-1" aria-labelledby="innocentiModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="innocentiModalLabel">Luca Innocenti's Talk</h5>
            </div>
            <div class="modal-body">
                <h6>Title: Connections Between Quantum Extreme Learning Machines, Quantum Reservoir Computing, and Shadow Tomography </h6>
                <p>Abstract: Quantum extreme learning machines (QELMs) and quantum reservoir computing (QRC) aim to efficiently post-process the outcomes of fixed—often uncalibrated—quantum devices to estimate properties of quantum states and solve related tasks. Shadow tomography, on the other hand, provides a methodology for estimating these properties without the resource scaling inherent in traditional tomography, utilizing measurement frames and the concept of dual measurements.<br>
                In this work, we present a unified framework that bridges QELMs, QRC, and shadow tomography by modeling them through effective measurements derived from general Positive Operator-Valued Measures (POVMs). We demonstrate that QELMs and QRCs can be concisely described via single effective measurements, providing an explicit characterization of the information retrievable with such protocols. Additionally, we show that the training process in QELMs closely parallels the reconstruction of effective measurements characterizing a given device.<br>
                Our approach reveals deep connections between these methodologies, highlighting how both can be viewed as quantum estimation techniques differing only in their assumptions about prior knowledge of the measurement apparatus. By leveraging the formalism of measurement frames, we examine the interplay between measurements, reconstructed observables, and estimators. This unified perspective paves the way for a more thorough understanding of the capabilities and limitations of QELMs, QRCs, and shadow tomography, potentially enhancing quantum state estimation methods to be more resilient to noise and imperfections while avoiding the dimensionality issues of traditional tomography.</p>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="Prati" tabindex="-1" aria-labelledby="pratiModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="pratiModalLabel">Enrico Prati's Talk</h5>
            </div>
            <div class="modal-body">
                <h6>Title: </h6>
                <p>Abstract: </p>
            </div>
        </div>
    </div>
</div>

<p class="text-center">
<a class="lead" href="../../">Back</a></p>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
    function setProportionalHeights(containerId) {
        const container = document.querySelector(`#${containerId} .program-container`);
        const events = container.querySelectorAll('.event-row');
        const containerHeight = container.offsetHeight;            
        let totalDuration = 0;
        events.forEach(event => {
            totalDuration += parseInt(event.dataset.duration);
        });            
        events.forEach(event => {
            const duration = parseInt(event.dataset.duration);
            const proportion = duration / totalDuration;
            event.style.height = `${containerHeight * proportion}px`;
        });
    }
    document.addEventListener('DOMContentLoaded', function() {
        const tabEls = document.querySelectorAll('button[data-bs-toggle="tab"]');
        tabEls.forEach(tabEl => {
            tabEl.addEventListener('shown.bs.tab', function(event) {
                const targetId = event.target.getAttribute('data-bs-target').substring(1);
                setProportionalHeights(targetId);
            });
        });            
        // Set heights for the initially active tab
        setProportionalHeights('day1');
    });
    document.addEventListener('DOMContentLoaded', function() {
        const speakerNames = document.querySelectorAll('.speaker-name');
        speakerNames.forEach(name => {
            name.addEventListener('click', function() {
                const modalId = this.getAttribute('data-bs-target');
                const modal = new bootstrap.Modal(document.querySelector(modalId));
                modal.show();
            });
        });
    });
</script>

</body>
</html>

<!--<html lang="en">
<!--<head>
<!--<title></title>
<!--<style>
<!--.nav-link[data-bs-target]:hover,
<!--.nav-link[data-bs-target].active {
<!--    color: #FFFFFF;
<!--    background-color: #3366CC;
<!--    border-color: var(--bs-btn-hover-border-color);
<!--}
<!--.event-row {
<!--    display: flex;
<!--    align-items: stretch;
<!--    margin-bottom: 1px;
<!--}
<!--.event-time {
<!--    width: 150px;
<!--    display: flex;
<!--    align-items: center;
<!--    justify-content: center;
<!--    text-align: center;
<!--    padding: 10px;
<!--}
<!--.event-description {
<!--    flex-grow: 1;
<!--    display: flex;
<!--    flex-direction: column;
<!--    justify-content: center;
<!--    text-align: center;
<!--    padding: 10px;
<!--}
<!--.blue-bg {
<!--    background-color: #3366CC;
<!--    color: white;
<!--}
<!--.gray-bg {
<!--    background-color: #7799AA;
<!--    color: white;
<!--}
<!--.light-gray-bg {
<!--    background-color: #f0f0f0;
<!--}
<!--.program-container {
<!--    height: 800px; /* Adjust this value to change the overall height of the schedule */
<!--}
<!--</style>
<!--</head>
<!--<body>
<!--  <h1><p style="text-align: center;">QRC2024</p></h1>
<!--  <p style="text-align: center;small">This Course is hosted at the</p>
<!--  <h4><p style="text-align: center;">ETTORE MAJORANA FOUNDATION AND CENTRE FOR SCIENTIFIC CULTURE</p></h4>
<!--  <p style="text-align: center;small">DIRECTOR: A. ZICHICHI</p>
<!--  <p style="text-align: center;small">as part of the</p>
<!--  <h2><p style="text-align: center;">INTERNATIONAL SCHOOL ON NONEQUILIBRIUM PHENOMENA</p></h2>
<!--  <p style="text-align: center;">Directors of the School: A. Lanzara, G. M. Palma, B. Spagnolo</p>
<!--  <br>
<!--  <h2><p style="text-align: center;color:#3366CC">Working Party on Quantum Reservoir Computing</p></h2>
<!--  <p style="text-align: center;">Directors of the Course: S. Lorenzo, G. M. Palma, M. Paternostro</p>
<!--  <p></p>
<!--  <p>Dates: 15 - 18 October 2024</p>
<!--  <p >
<!--    The aim of the course is to discuss the current understanding of quantum reservoir computing and to develop characterization tools for quantum <!--computation and process identification. The features of specific platforms currently being explored for these goals will be considered, as well as the <!--impact of noise and thermodynamic constraints. <br> The working party will discuss the range of tasks that can be efficiently solved by QRC and, <!--notably, the combination of analytical and numerical approaches, including the exploitation of quantum simulation on quantum computing platforms.
<!--  </p>
<!--  <p>If you want to join us, please <a href="https://docs.google.com/forms/d/16PHgeI1JZ3a76JzZBJH7RkPYNi6iKZcnkFfdmD1T6Bw/edit?<!--ts=66f3e6eb#response=ACYDBNjvW-b0BZf63AWMP9PsBHFWIgcsYo5Gsa-BvJ0S21nzUB6mktHnY1RX4NluflDVXMc">REGISTER</a>.</p>
<!--  <!---<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet"/>-->
<!--  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>
<!--  <div class="container py-12 py-lg-12 position-relative z-index-0">
<!--    <div class="col-lg-12 mb-12 mb-lg-0">
<!--        <h1 style="text-align: center; color:Black" class="mb-4  aos-init aos-animate" data-aos="fade-up">
<!--            Program
<!--        </h1>
<!--    </div>
<!--    <div class="d-flex justify-content-center">
<!--    <ul class="nav nav-pills mb-3 justify-content-center" id="myTab" role="tablist">
<!--        <li class="nav-item" role="presentation">
<!--            <button class="nav-link active" id="d1-tab" data-bs-toggle="tab" data-bs-target="#day1" type="button" role="tab" aria-controls="day1" <!--aria-selected="true">Day 1 (Oct 15)</button>
<!--        </li>
<!--        <li class="nav-item" role="presentation">
<!--            <button class="nav-link" id="d2-tab" data-bs-toggle="tab" data-bs-target="#day2" type="button" role="tab" aria-controls="day2" <!--aria-selected="false">Day 2 (Oct 16)</button>
<!--        </li>
<!--        <li class="nav-item" role="presentation">
<!--            <button class="nav-link" id="d3-tab" data-bs-toggle="tab" data-bs-target="#day3" type="button" role="tab" aria-controls="day3" <!--aria-selected="false">Day 3 (Oct 17)</button>
<!--        </li>
<!--        <li class="nav-item" role="presentation">
<!--            <button class="nav-link" id="d4-tab" data-bs-toggle="tab" data-bs-target="#day4" type="button" role="tab" aria-controls="day4" <!--aria-selected="false">Day 4 (Oct 18)</button>
<!--        </li>
<!--    </ul>
<!--    </div>
<!--    <div class="col-lg-12 col-xl-12" >
<!--        <div  data-aos="fade-up" class="tab-content aos-init aos-animate" id="myTabContent">
<!--            <!---------------GIORNO 1----------------->
<!--            <div class="tab-pane fade active show" id="day1" role="tabpanel" aria-labelledby="d1-tab">
<!--                <ul class="pt-4 list-unstyled mb-0">
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center" style="gap:50px;background-color:#3366CC; color:white">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            <br>
<!--                            <br>
<!--                            <br>
<!--                            <br>
<!--                            9:00 AM - 12:30 AM
<!--                            <br>
<!--                            <br>
<!--                            <br>
<!--                            <br>
<!--                            <br>
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                             Arrivals, opening and registration
<!--                            <!--<p class="mb-0"></p>-->
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            <br>
<!--                            <br>  
<!--                            12:30 - 15:00
<!--                            <br>
<!--                            <br>
<!--                            <br>
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Lunch
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center" style="gap:50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            15:00 - 15:50
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Oliver Neill</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">  
<!--                            15:50 - 16:20
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Coffe break
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap:50px;background-color:rgb(220,220,220);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            16:20 - 17:10
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Marco Pezzutto</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            17:10 - 18:00
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Francesco Plastina</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                </ul>
<!--            </div>
<!--            <!---------------GIORNO 2----------------->
<!--            <div class="tab-pane fade" id="day2" role="tabpanel" aria-labelledby="d2-tab">
<!--                <ul class="pt-4 list-unstyled mb-0">
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center" style="gap:50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            9:00 - 9:50
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Valeria Cimini</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap:50px;background-color:rgb(220,220,220);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            9:50 - 10:40
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Andrea Smirne</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">  
<!--                            10:40 - 11:10
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Coffe break
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            11:10 - 12:00
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Alessandro Romancino</h4>
<!--                            <p class="mb-1 small">Entanglement Percolation in Random State Quantum Networks</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            <br>
<!--                            <br>  
<!--                            12:00 - 15:00
<!--                            <br>
<!--                            <br>
<!--                            <br>
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Lunch
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center" style="gap:50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            15:00 - 15:50
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Antonio Sannia</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">  
<!--                            15:50 - 16:20
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Coffe break
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap:50px;background-color:rgb(220,220,220);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            16:20 - 17:10
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Gabriele Lo Monaco</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            17:10 - 18:00
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Alessandro Ferraro</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                </ul>
<!--            </div>
<!--            <!---------------GIORNO 3----------------->
<!--            <div class="tab-pane fade" id="day3" role="tabpanel" aria-labelledby="d3-tab">
<!--                <ul class="pt-4 list-unstyled mb-0">
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center" style="gap:50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            9:00 - 9:50
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Sofia Sgroi</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap:50px;background-color:rgb(220,220,220);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            9:50 - 10:40
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Dario Tamascelli</h4>
<!--                            <p class="mb-1 small">Spectral Density Modulation and Universal Markovian Closure of Structured Environments</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">  
<!--                            10:40 - 11:10
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Coffe break
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            11:10 - 12:00
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Davide Rattacaso</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            <br>
<!--                            <br>  
<!--                            12:00 - 15:00
<!--                            <br>
<!--                            <br>
<!--                            <br>
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Lunch
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center" style="gap:50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            15:00 - 15:50
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Alessandra Colla</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">  
<!--                            15:50 - 16:20
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Coffe break
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap:50px;background-color:rgb(220,220,220);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            16:20 - 17:10
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Iris Agresti</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            17:10 - 18:00
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Marco Vetrano</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                </ul>
<!--            </div>
<!--            <!---------------GIORNO 4----------------->
<!--            <div class="tab-pane fade" id="day4" role="tabpanel" aria-labelledby="d4-tab">
<!--                <ul class="pt-4 list-unstyled mb-0">
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center" style="gap:50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            9:00 - 9:50
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Tomasz Paterek</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap:50px;background-color:rgb(220,220,220);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            9:50 - 10:40
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Luca Innocenti</h4>
<!--                            <p class="mb-1 small"> Connections Between Quantum Extreme Learning Machines, Quantum Reservoir Computing, and Shadow <!--Tomography</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">  
<!--                            10:40 - 11:10
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Coffe break
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:rgb(240,240,240);">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            11:10 - 12:00
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            <h4>Enrico Prati</h4>
<!--                            <p class="mb-1 small">QRC2024</p>
<!--                        </span>
<!--                    </li>
<!--                    <li class="d-flex flex-column flex-md-row py-0 align-items-center " style="gap: 50px;background-color:#7799AA; color:white">
<!--                        <span style="text-align:center; width: 250px;">
<!--                            <br>
<!--                            <br>  
<!--                            12:00 - 15:00
<!--                            <br>
<!--                            <br>
<!--                            <br>
<!--                        </span>
<!--                        <span style="text-align:center; width: 450px;">
<!--                            Closing & Lunch
<!--                        </span>
<!--                    </li>
<!--                </ul>
<!--            </div>
<!--        </div>
<!--    </div>
<!--  </div>
<!--    <p class="text-center">
<!--    <a class="lead" href="../../">Back</a></p>
<!--    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>
<!--<script>
<!--    function setProportionalHeights(containerId) {
<!--        const container = document.querySelector(`#${containerId} .program-container`);
<!--        const events = container.querySelectorAll('.event-row');
<!--        const containerHeight = container.offsetHeight;            
<!--        let totalDuration = 0;
<!--        events.forEach(event => {
<!--            totalDuration += parseInt(event.dataset.duration);
<!--        });            
<!--        events.forEach(event => {
<!--            const duration = parseInt(event.dataset.duration);
<!--            const proportion = duration / totalDuration;
<!--            event.style.height = `${containerHeight * proportion}px`;
<!--        });
<!--    }
<!--    document.addEventListener('DOMContentLoaded', function() {
<!--        const tabEls = document.querySelectorAll('button[data-bs-toggle="tab"]');
<!--        tabEls.forEach(tabEl => {
<!--            tabEl.addEventListener('shown.bs.tab', function(event) {
<!--                const targetId = event.target.getAttribute('data-bs-target').substring(1);
<!--                setProportionalHeights(targetId);
<!--            });
<!--        });            
<!--        // Set heights for the initially active tab
<!--        setProportionalHeights('day1');
<!--    });
<!--</script>
<!--</body>
<!--</html>
