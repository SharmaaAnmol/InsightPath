import { test, describe } from "node:test";
import assert from "node:assert";
import { submitAssessment, type AssessmentRequest } from "../lib/api.ts";

describe("Frontend Career-Readiness Assessment", () => {
  test("submits high-performing profile and maps to Q1 with ethical language", async () => {
    const payload: AssessmentRequest = {
      career_goal: "Data Scientist",
      experience_level: "Junior (2-4 years)",
      maths_stats_skills: 4.8,
      coding_skills: 4.6,
      ai_and_ml_skills: 4.8,
      big_data_skills: 4.2,
      dashboard_and_storytelling_skills: 4.5,
    };

    const { data } = await submitAssessment(payload);

    // Verify structural profile
    assert.strictEqual(data.career_goal, "Data Scientist");
    assert.strictEqual(data.quadrant_assigned, "Q1");
    assert.ok(data.model_probability >= 0.5);
    assert.ok(data.model_signal.includes("Observed-model signal"));

    // Verify Radar points
    assert.strictEqual(data.radar_data.length, 5);
    assert.strictEqual(data.recommendations.length, 5);
    assert.strictEqual(data.learning_sequence.length, 3);

    // Strict Ethical Language Tests
    const text = JSON.stringify(data);
    assert.strictEqual(text.includes("You will get a high salary"), false);
    assert.strictEqual(text.includes("You are guaranteed to succeed"), false);
    assert.strictEqual(text.includes("You are suitable for hiring"), false);
    assert.ok(text.includes("Based on the observed JDS cohort") || text.includes("observed JDS cohort"));
    assert.ok(data.methodology_disclaimer.includes("METHODOLOGY & ETHICAL NOTICE"));
  });

  test("submits execution-heavy profile and flags storytelling as development priority (Q2)", async () => {
    const payload: AssessmentRequest = {
      career_goal: "Machine Learning Engineer",
      experience_level: "Junior (2-4 years)",
      maths_stats_skills: 4.6,
      coding_skills: 4.7,
      ai_and_ml_skills: 4.5,
      big_data_skills: 4.0,
      dashboard_and_storytelling_skills: 2.1,
    };

    const { data } = await submitAssessment(payload);

    assert.strictEqual(data.quadrant_assigned, "Q2");
    assert.ok(data.quadrant_title.includes("Execution Specialist"));
    assert.ok(data.priority_skills.includes("Dashboarding & Storytelling"));
    assert.ok(
      data.development_gaps.some((g) => g.includes("Dashboarding & Storytelling"))
    );
  });

  test("submits foundational profile and maps to Q4 with developmental sequence", async () => {
    const payload: AssessmentRequest = {
      career_goal: "Data Analyst",
      experience_level: "Entry-Level (0-2 years)",
      maths_stats_skills: 2.2,
      coding_skills: 2.5,
      ai_and_ml_skills: 2.0,
      big_data_skills: 2.0,
      dashboard_and_storytelling_skills: 2.2,
    };

    const { data } = await submitAssessment(payload);

    assert.strictEqual(data.quadrant_assigned, "Q4");
    assert.ok(data.quadrant_title.includes("Foundational Development"));
    assert.strictEqual(data.learning_sequence.length, 3);
    assert.ok(data.learning_sequence[0].milestone.length > 0);
  });
});
