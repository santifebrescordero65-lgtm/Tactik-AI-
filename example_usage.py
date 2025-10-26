"""
TACTIK AI 5.3 - Example Usage
Demonstrates the Ecuador → Europe banana export negotiation case study
"""

from tactik_algorithm import (
    TACTIKEngine,
    GroundTruthSource,
    create_ground_truth_source
)


def main():
    """
    Example: Simulating negotiation with CEO EDEKA for Ecuador banana exports
    """

    # Initialize TACTIK Engine
    engine = TACTIKEngine()

    print("═" * 70)
    print("TACTIK AI 5.3 PREMIUM - Ecuador → EDEKA Banana Export Simulation")
    print("═" * 70)
    print()

    # ═══════════════════════════════════════════════════════════════════
    # STEP 1: Build Ground Truth Sources for CEO EDEKA
    # ═══════════════════════════════════════════════════════════════════

    print("STEP 1: Building Ground Truth Sources...")
    print()

    sources_edeka = [
        # TIER 1 PRIMARY (100% weight)
        create_ground_truth_source(
            source_id="source_001",
            tier="tier_1_primary",
            description="Ley Cadena Suministro Alemania (Lieferkettengesetz)",
            url="https://www.gesetze-im-internet.de/lksg/",
            date="2023-01-01",
            cross_verified=True
        ),

        # TIER 2 SECONDARY (85% weight)
        create_ground_truth_source(
            source_id="source_002",
            tier="tier_2_secondary",
            description="Denuncias Oxfam 2023 contra EDEKA",
            url="https://www.ecchr.eu/en/case/edeka-und-rewe-verstossen-gegen-lieferkettengesetz/",
            date="2023-12-11",
            cross_verified=True
        ),

        create_ground_truth_source(
            source_id="source_003",
            tier="tier_2_secondary",
            description="Proyecto WWF-EDEKA 2014-2019 banano sostenible",
            url="https://www.wwf.mg/?356695%2Fbananosostenible",
            date="2019-12-02",
            cross_verified=True
        ),

        create_ground_truth_source(
            source_id="source_004",
            tier="tier_2_secondary",
            description="Perfil LinkedIn Markus Mosa (CEO EDEKA)",
            url="https://www.linkedin.com/in/markusmosa",
            date="2024-08-15",
            cross_verified=False
        ),

        create_ground_truth_source(
            source_id="source_005",
            tier="tier_2_secondary",
            description="Informe Anual EDEKA 2023 - Compromiso Sostenibilidad",
            url="https://www.edeka.de/nachhaltigkeit/bericht-2023.pdf",
            date="2024-03-20",
            cross_verified=False
        ),

        # TIER 3 TERTIARY (60% weight)
        create_ground_truth_source(
            source_id="source_006",
            tier="tier_3_tertiary",
            description="Análisis mercado banano Alemania - Fruchthandel Magazine",
            date="2024-01-15",
            cross_verified=False
        ),

        create_ground_truth_source(
            source_id="source_007",
            tier="tier_3_tertiary",
            description="Entrevista CEO EDEKA - Lebensmittelzeitung",
            date="2023-06-10",
            cross_verified=False
        ),

        # TIER 4 INFERRED (40% weight)
        create_ground_truth_source(
            source_id="source_008",
            tier="tier_4_inferred",
            description="Presión competitiva ALDI/LIDL (inferido análisis mercado)",
            date="2024-09-01",
            cross_verified=False
        )
    ]

    print(f"✓ Created {len(sources_edeka)} ground truth sources")
    print(f"  - Tier 1 Primary: 1 source")
    print(f"  - Tier 2 Secondary: 4 sources")
    print(f"  - Tier 3 Tertiary: 2 sources")
    print(f"  - Tier 4 Inferred: 1 source")
    print(f"  - Cross-verified: {sum(1 for s in sources_edeka if s.cross_verified)} sources")
    print()

    # ═══════════════════════════════════════════════════════════════════
    # STEP 2: Build Avatar DNA for CEO EDEKA
    # ═══════════════════════════════════════════════════════════════════

    print("STEP 2: Building Avatar DNA for CEO EDEKA...")
    print()

    # Influences (verified vs inferred)
    influences_verified = [
        {
            "influence": "Ley Cadena Suministro obliga due diligence",
            "source_id": "source_001",
            "impact": "high"
        },
        {
            "influence": "Denuncia Oxfam 2023 genera presión reputacional",
            "source_id": "source_002",
            "impact": "high"
        },
        {
            "influence": "Precedente WWF 2014-2019 muestra modelo exitoso",
            "source_id": "source_003",
            "impact": "medium"
        }
    ]

    influences_inferred = [
        {
            "influence": "Presión competitiva ALDI/LIDL en precio",
            "rationale": "Inferido desde análisis cuota mercado"
        }
    ]

    # Thoughts (verified patterns)
    thoughts_verified = [
        {
            "thought": "Sostenibilidad es prioridad estratégica (compromiso 100% banano sostenible 2025)",
            "source_id": "source_005"
        },
        {
            "thought": "Riesgo legal bajo Lieferkettengesetz requiere certificación proveedores",
            "source_id": "source_001"
        }
    ]

    thoughts_inferred = [
        {
            "thought": "Balance entre sostenibilidad y competitividad precio",
            "rationale": "Inferido desde contexto retail alemán"
        }
    ]

    # Behavioral patterns
    behavioral_verified = [
        {
            "behavior": "Pausó compras proveedores sin certificación post-denuncia Oxfam",
            "source_id": "source_002",
            "context": "Respuesta legal proactiva"
        },
        {
            "behavior": "Colaboró 5 años con WWF en proyecto piloto sostenibilidad",
            "source_id": "source_003",
            "context": "Disposición partnerships largo plazo"
        }
    ]

    behavioral_inferred = [
        {
            "behavior": "Negociación basada en datos técnicos y ROI medible",
            "rationale": "Estándar industria retail alemana"
        }
    ]

    # Decision style
    decision_verified = [
        {
            "style": "Risk-averse bajo marco legal",
            "source_id": "source_001"
        }
    ]

    decision_inferred = [
        {
            "style": "Data-driven con enfoque largo plazo",
            "rationale": "Perfil típico CEO retail alemán"
        }
    ]

    # Communication style
    communication_verified = [
        {
            "style": "Profesional, directo, enfocado en compliance",
            "source_id": "source_007"
        }
    ]

    communication_inferred = []

    # Priorities
    priorities_verified = [
        {
            "priority": "1. Compliance legal (Lieferkettengesetz)",
            "source_id": "source_001"
        },
        {
            "priority": "2. Reputación sostenibilidad",
            "source_id": "source_005"
        }
    ]

    priorities_inferred = [
        {
            "priority": "3. Competitividad precio vs ALDI/LIDL",
            "rationale": "Contexto mercado"
        }
    ]

    # Build complete DNA
    dna_edeka = engine.build_avatar_dna(
        avatar_id="ceo_edeka",
        avatar_name="Markus Mosa (CEO EDEKA)",
        role="Chief Executive Officer - EDEKA Zentrale",
        sources=sources_edeka,
        influences_verified=influences_verified,
        influences_inferred=influences_inferred,
        thoughts_verified=thoughts_verified,
        thoughts_inferred=thoughts_inferred,
        behavioral_verified=behavioral_verified,
        behavioral_inferred=behavioral_inferred,
        decision_style_verified=decision_verified,
        decision_style_inferred=decision_inferred,
        communication_verified=communication_verified,
        communication_inferred=communication_inferred,
        priorities_verified=priorities_verified,
        priorities_inferred=priorities_inferred,
        environment="Retail alemán altamente competitivo, marco legal Lieferkettengesetz, presión ONGs",
        constraints={
            "legal": "Obligación due diligence cadena suministro",
            "reputacional": "Exposición pública post-denuncia Oxfam",
            "comercial": "Presión precio de competidores discount"
        },
        language="es"
    )

    print(f"✓ Avatar DNA created: {dna_edeka.avatar_name}")
    print(f"  - Role: {dna_edeka.role}")
    print(f"  - Sources: {len(dna_edeka.sources)}")

    # Calculate source coverage
    coverage, breakdown = dna_edeka.calculate_source_coverage()
    print(f"  - Source Coverage: {coverage*100:.1f}%")
    print(f"    • Influences: {breakdown['influences']*100:.1f}%")
    print(f"    • Thoughts: {breakdown['thoughts']*100:.1f}%")
    print(f"    • Behavioral: {breakdown['behavioral_pattern']*100:.1f}%")
    print(f"    • Decision Style: {breakdown['decision_style']*100:.1f}%")
    print()

    # ═══════════════════════════════════════════════════════════════════
    # STEP 3: Calculate AVDA Validation Metrics
    # ═══════════════════════════════════════════════════════════════════

    print("STEP 3: Calculating AVDA Validation Metrics...")
    print()

    avda_metrics = engine.calculate_avda_score("ceo_edeka")
    avda_display = avda_metrics.to_percentage()

    print(f"┌{'─' * 68}┐")
    print(f"│ AVDA VALIDATION RESULTS - CEO EDEKA                              │")
    print(f"├{'─' * 68}┤")
    print(f"│ AVDA Score:            {avda_display['avda_score']:>5.1f}% - {avda_metrics.classification.value:<26} │")
    print(f"│ Confidence Interval:   [{avda_display['confidence_interval'][0]:>5.1f}% - {avda_display['confidence_interval'][1]:>4.1f}%] (95% CI)           │")
    print(f"├{'─' * 68}┤")
    print(f"│ Component Breakdown:                                             │")
    print(f"│   • Accuracy:          {avda_display['accuracy']:>5.1f}%                                       │")
    print(f"│   • Source Coverage:   {avda_display['source_coverage']:>5.1f}%                                       │")
    print(f"│   • Drift Risk:        {avda_display['drift_risk']:>5.1f}%                                       │")
    print(f"│   • GT Quality:        {avda_display['ground_truth_quality']:>5.1f}%                                       │")
    print(f"└{'─' * 68}┘")
    print()

    print("RECOMMENDATION:")
    print(f"  {avda_metrics.get_recommendation()}")
    print()

    if avda_metrics.limitations:
        print("LIMITATIONS:")
        for limitation in avda_metrics.limitations:
            print(f"  {limitation}")
        print()

    # ═══════════════════════════════════════════════════════════════════
    # STEP 4: Create Multi-Avatar Simulation Session
    # ═══════════════════════════════════════════════════════════════════

    print("STEP 4: Creating Multi-Avatar Simulation Session...")
    print()

    session = engine.create_multi_avatar_session(
        session_id="session_001",
        user_goal="Preparar negociación exportación banano Ecuador → EDEKA Alemania",
        avatar_ids=["ceo_edeka"]
    )

    print(f"✓ Session created: {session.session_id}")
    print(f"  - Goal: {session.user_goal}")
    print(f"  - Active avatars: {len(session.active_avatars)}")
    print()

    # ═══════════════════════════════════════════════════════════════════
    # STEP 5: Simulate Conversation Turns (simplified)
    # ═══════════════════════════════════════════════════════════════════

    print("STEP 5: Simulating Conversation Turns...")
    print()

    # Simulate 5 turns as example
    sample_messages = [
        "¿Cuál es la posición de EDEKA sobre proveedores Ecuador post-denuncia Oxfam?",
        "¿Qué certificaciones específicas requiere EDEKA para reactivar compras?",
        "¿Hay interés en replicar modelo WWF 2014-2019 con nuevos proveedores?",
        "¿Qué volumen de compra podría considerar EDEKA en proyecto piloto?",
        "¿Cuál sería timeline ideal para implementación desde perspectiva EDEKA?"
    ]

    for i, msg in enumerate(sample_messages, 1):
        print(f"Turn {i}:")
        print(f"  User: {msg}")

        result = engine.orchestrate_turn(
            session_id="session_001",
            speaker_id="ceo_edeka",
            message=msg
        )

        if result["action"] == "EMPATHY_PAUSE":
            print(f"  [EMPATHY PAUSE] {result['message']}")
        elif result["action"] == "GATING_INTERRUPTED":
            print(f"  [GATING] Response regenerated (quality threshold)")
        else:
            turn = result["turn"]
            print(f"  CEO EDEKA: [Response simulated - turn {turn.turn_number}]")
            print(f"    Scores: EIS={turn.eis_score:.2f}, HCA={turn.hca_score:.2f}, DNA={turn.dna_score:.2f}")

            if result["backflow_triggered"]:
                print(f"    [BACKFLOW] {result['backflow_issue']} detected - recalibrating")

        print()

    # ═══════════════════════════════════════════════════════════════════
    # STEP 6: Generate TACTIK Advisor Report
    # ═══════════════════════════════════════════════════════════════════

    print("═" * 70)
    print("STEP 6: Generating TACTIK Advisor Report...")
    print("═" * 70)
    print()

    advisor_report = engine.generate_tactik_advisor("session_001")

    print("SESSION SUMMARY:")
    print(f"  - Session ID: {advisor_report['session_summary']['session_id']}")
    print(f"  - Goal: {advisor_report['session_summary']['goal']}")
    print(f"  - Total Turns: {advisor_report['session_summary']['total_turns']}")
    print(f"  - TACTIK Score: {advisor_report['session_summary']['tactik_score']}/10")
    print(f"  - Duration: {advisor_report['session_summary']['duration']}")
    print()

    print("AVATAR VALIDATION:")
    for avatar_id, avda in advisor_report['avatar_avda_scores'].items():
        print(f"  - {avatar_id}: {avda['avda_score']}% ({avda['classification']})")
    print()

    print("KEY INSIGHTS:")
    for insight in advisor_report['key_insights']:
        print(f"  • {insight}")
    print()

    print("RECOMMENDATIONS:")
    for rec in advisor_report['recommendations']:
        print(f"  {rec}")
    print()

    print("72-HOUR ACTION PLAN:")
    for action in advisor_report['action_plan_72h']:
        print(f"  [{action['timeframe']}] {action['action']} (Priority: {action['priority']})")
    print()

    print("TRANSPARENCY CARD:")
    tc = advisor_report['transparency_card']
    print(f"  Certification: {tc['certification']}")
    print(f"  Session ID: {tc['session_id']}")
    print(f"  Timestamp: {tc['timestamp']}")
    print(f"  Quality Assurance:")
    print(f"    - Empathy Pauses: {tc['quality_assurance']['empathy_pauses']}")
    print(f"    - Backflow Corrections: {tc['quality_assurance']['backflow_corrections']}")
    print(f"    - Avg TACTIK Score: {tc['quality_assurance']['avg_tactik_score']}")
    print(f"  Overall Recommendation: {tc['usage_guidelines']['recommended_use']}")
    print()

    print("═" * 70)
    print("TACTIK AI 5.3 - Simulation Complete")
    print("═" * 70)


if __name__ == "__main__":
    main()
