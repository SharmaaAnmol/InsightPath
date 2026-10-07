-- ==============================================================================
-- Supabase Migration: User Profiles, Assessments, and Career Roadmaps
-- InsightPath / RUSTY WOLVES Analytics Web Platform
-- ==============================================================================
-- Description:
-- Implements authentication-linked persistent career profiles, assessment history,
-- radar skill scores, career goals, and interactive roadmap state.
-- All tables enforce strict PostgreSQL Row Level Security (RLS) to isolate user data.
-- Public ML models and analytical outputs remain strictly read-only and uncoupled.
-- ==============================================================================

-- 1. PROFILES TABLE (linked 1:1 with auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    full_name TEXT,
    avatar_url TEXT,
    target_role TEXT DEFAULT 'Data Scientist',
    experience_level TEXT DEFAULT 'Junior (2-4 years)',
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 2. CAREER GOALS TABLE
CREATE TABLE IF NOT EXISTS public.career_goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    target_role TEXT NOT NULL DEFAULT 'Data Scientist',
    experience_level TEXT NOT NULL DEFAULT 'Junior (2-4 years)',
    target_timeline TEXT DEFAULT '6-12 months',
    target_salary_lakh NUMERIC(5, 2) DEFAULT 18.5,
    key_focus_areas TEXT[] DEFAULT ARRAY['Model Interpretability', 'Executive Storytelling'],
    notes TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 3. ASSESSMENTS TABLE (History of completed empirical diagnostics)
CREATE TABLE IF NOT EXISTS public.assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    career_goal TEXT NOT NULL,
    experience_level TEXT NOT NULL,
    model_signal TEXT NOT NULL,
    model_probability NUMERIC(5, 4) NOT NULL,
    quadrant_assigned TEXT NOT NULL,
    quadrant_title TEXT NOT NULL,
    recommendation_summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 4. ASSESSMENT SCORES TABLE (Detailed breakdown per skill dimension)
CREATE TABLE IF NOT EXISTS public.assessment_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES public.assessments(id) ON DELETE CASCADE,
    skill_key TEXT NOT NULL,
    skill_label TEXT NOT NULL,
    user_score NUMERIC(3, 2) NOT NULL,
    cohort_benchmark NUMERIC(3, 2) NOT NULL,
    gap NUMERIC(4, 2) NOT NULL,
    importance_rank INT NOT NULL
);

-- 5. ROADMAP ITEMS TABLE (User milestone tracking & progression)
CREATE TABLE IF NOT EXISTS public.roadmap_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    stage_id TEXT NOT NULL, -- e.g. 'stage-1', 'stage-2', 'stage-3', 'stage-4'
    title TEXT NOT NULL,
    description TEXT,
    milestone_order INT NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'completed')),
    target_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ==============================================================================
-- INDEXES FOR PERFORMANCE & QUERY ACCELERATION
-- ==============================================================================
CREATE INDEX IF NOT EXISTS idx_career_goals_user ON public.career_goals(user_id);
CREATE INDEX IF NOT EXISTS idx_assessments_user_created ON public.assessments(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_assessment_scores_assessment ON public.assessment_scores(assessment_id);
CREATE INDEX IF NOT EXISTS idx_roadmap_items_user_stage ON public.roadmap_items(user_id, stage_id);

-- ==============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ==============================================================================

-- Enable RLS on all 5 tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.career_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.assessment_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.roadmap_items ENABLE ROW LEVEL SECURITY;

-- 1. PROFILES POLICIES
DROP POLICY IF EXISTS "Users can view their own profile" ON public.profiles;
CREATE POLICY "Users can view their own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

DROP POLICY IF EXISTS "Users can update their own profile" ON public.profiles;
CREATE POLICY "Users can update their own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

DROP POLICY IF EXISTS "Users can insert their own profile" ON public.profiles;
CREATE POLICY "Users can insert their own profile"
    ON public.profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "Users can delete their own profile" ON public.profiles;
CREATE POLICY "Users can delete their own profile"
    ON public.profiles FOR DELETE
    USING (auth.uid() = id);

-- 2. CAREER GOALS POLICIES
DROP POLICY IF EXISTS "Users can manage their own career goals (select)" ON public.career_goals;
CREATE POLICY "Users can manage their own career goals (select)"
    ON public.career_goals FOR SELECT
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can manage their own career goals (insert)" ON public.career_goals;
CREATE POLICY "Users can manage their own career goals (insert)"
    ON public.career_goals FOR INSERT
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can manage their own career goals (update)" ON public.career_goals;
CREATE POLICY "Users can manage their own career goals (update)"
    ON public.career_goals FOR UPDATE
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can manage their own career goals (delete)" ON public.career_goals;
CREATE POLICY "Users can manage their own career goals (delete)"
    ON public.career_goals FOR DELETE
    USING (auth.uid() = user_id);

-- 3. ASSESSMENTS POLICIES
DROP POLICY IF EXISTS "Users can view their own assessments" ON public.assessments;
CREATE POLICY "Users can view their own assessments"
    ON public.assessments FOR SELECT
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert their own assessments" ON public.assessments;
CREATE POLICY "Users can insert their own assessments"
    ON public.assessments FOR INSERT
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete their own assessments" ON public.assessments;
CREATE POLICY "Users can delete their own assessments"
    ON public.assessments FOR DELETE
    USING (auth.uid() = user_id);

-- 4. ASSESSMENT SCORES POLICIES (Enforce parent assessment ownership)
DROP POLICY IF EXISTS "Users can view their own assessment scores" ON public.assessment_scores;
CREATE POLICY "Users can view their own assessment scores"
    ON public.assessment_scores FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.assessments a
            WHERE a.id = assessment_scores.assessment_id
              AND a.user_id = auth.uid()
        )
    );

DROP POLICY IF EXISTS "Users can insert their own assessment scores" ON public.assessment_scores;
CREATE POLICY "Users can insert their own assessment scores"
    ON public.assessment_scores FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.assessments a
            WHERE a.id = assessment_scores.assessment_id
              AND a.user_id = auth.uid()
        )
    );

DROP POLICY IF EXISTS "Users can delete their own assessment scores" ON public.assessment_scores;
CREATE POLICY "Users can delete their own assessment scores"
    ON public.assessment_scores FOR DELETE
    USING (
        EXISTS (
            SELECT 1 FROM public.assessments a
            WHERE a.id = assessment_scores.assessment_id
              AND a.user_id = auth.uid()
        )
    );

-- 5. ROADMAP ITEMS POLICIES
DROP POLICY IF EXISTS "Users can view their own roadmap items" ON public.roadmap_items;
CREATE POLICY "Users can view their own roadmap items"
    ON public.roadmap_items FOR SELECT
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert their own roadmap items" ON public.roadmap_items;
CREATE POLICY "Users can insert their own roadmap items"
    ON public.roadmap_items FOR INSERT
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update their own roadmap items" ON public.roadmap_items;
CREATE POLICY "Users can update their own roadmap items"
    ON public.roadmap_items FOR UPDATE
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can delete their own roadmap items" ON public.roadmap_items;
CREATE POLICY "Users can delete their own roadmap items"
    ON public.roadmap_items FOR DELETE
    USING (auth.uid() = user_id);

-- ==============================================================================
-- AUTOMATED PROFILE CREATION TRIGGER ON AUTH SIGNUP
-- ==============================================================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, avatar_url)
    VALUES (
        new.id,
        new.email,
        COALESCE(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1)),
        new.raw_user_meta_data->>'avatar_url'
    )
    ON CONFLICT (id) DO NOTHING;

    -- Create default career goal
    INSERT INTO public.career_goals (user_id, target_role, experience_level)
    VALUES (new.id, 'Data Scientist', 'Junior (2-4 years)')
    ON CONFLICT DO NOTHING;

    -- Create default initial roadmap items from Phase 8 Career Framework
    INSERT INTO public.roadmap_items (user_id, stage_id, title, description, milestone_order, status)
    VALUES
        (new.id, 'stage-1', 'Python & Pandas Scalability Audits', 'Master vectorization, memory optimization, and unit testing pipelines.', 1, 'in_progress'),
        (new.id, 'stage-1', 'Statistical Rigor: Inferential Testing', 'Conduct Mann-Whitney U, Chi-Square, and Cohen''s d effect size analyses.', 2, 'todo'),
        (new.id, 'stage-2', 'Interpretable Machine Learning Models', 'Train and evaluate Logistic Regression (L2) with Odds Ratio extraction.', 3, 'todo'),
        (new.id, 'stage-2', 'Executive Storytelling & Visualization', 'Translate complex ROC-AUC and feature importance into business trade-offs.', 4, 'todo'),
        (new.id, 'stage-3', 'Cross-Domain Strategic Synthesis', 'Bridge technical analytics with organizational decision-making matrix.', 5, 'todo')
    ON CONFLICT DO NOTHING;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
