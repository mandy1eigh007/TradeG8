-- TradeG8 Database Schema
-- Run this in your Supabase SQL editor to set up the complete database.
-- Built by Mandy Richardson & Claude (Anthropic)

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL DEFAULT 'student' CHECK (role IN ('student', 'case_manager', 'admin')),
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    case_manager_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Jobs table
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    pay TEXT,
    url TEXT,
    source TEXT,
    description TEXT,
    posted_date TIMESTAMP,

    -- L&I Verification fields
    lni_registered BOOLEAN DEFAULT false,
    lni_status TEXT,
    lni_licensed_electrical BOOLEAN DEFAULT false,
    lni_licensed_plumbing BOOLEAN DEFAULT false,
    lni_violations INTEGER DEFAULT 0,
    lni_workers_comp TEXT,

    -- Glassdoor fields
    glassdoor_rating DECIMAL,
    glassdoor_review_count INTEGER,
    glassdoor_summary TEXT,

    -- Scoring
    score INTEGER DEFAULT 0,
    score_breakdown TEXT,
    hours_count_toward_trainee BOOLEAN DEFAULT false,
    recommendation TEXT,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Saved jobs table for student tracking
CREATE TABLE saved_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'saved' CHECK (status IN ('saved', 'applied', 'interview', 'offer', 'rejected')),
    notes TEXT,
    applied_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, job_id)
);

-- Resumes table
CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    trade_focus TEXT,
    content JSONB,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Activity logs table for compliance reporting
CREATE TABLE activity_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_type TEXT NOT NULL,
    details JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Case notes table from case manager to student
CREATE TABLE case_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    case_manager_id UUID REFERENCES users(id) ON DELETE CASCADE,
    note TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Compliance reports table
CREATE TABLE compliance_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    report_type TEXT NOT NULL,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    data JSONB,
    generated_at TIMESTAMP DEFAULT NOW()
);

-- Companies table for partnership tracking
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    lni_status TEXT,
    glassdoor_rating DECIMAL,
    contact_email TEXT,
    contact_phone TEXT,
    partnership_status TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_jobs_company ON jobs(company);
CREATE INDEX idx_jobs_score ON jobs(score DESC);
CREATE INDEX idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX idx_saved_jobs_user_id ON saved_jobs(user_id);
CREATE INDEX idx_saved_jobs_status ON saved_jobs(status);
CREATE INDEX idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_timestamp ON activity_logs(timestamp DESC);
CREATE INDEX idx_case_notes_user_id ON case_notes(user_id);
CREATE INDEX idx_case_notes_case_manager_id ON case_notes(case_manager_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers to tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_saved_jobs_updated_at BEFORE UPDATE ON saved_jobs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_resumes_updated_at BEFORE UPDATE ON resumes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert test data (optional - comment out if not needed)
-- INSERT INTO users (email, role, first_name, last_name) VALUES
-- ('student@tradeg8.test', 'student', 'Test', 'Student'),
-- ('manager@tradeg8.test', 'case_manager', 'Case', 'Manager');

-- Grant permissions (adjust as needed for your setup)
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE saved_jobs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE case_notes ENABLE ROW LEVEL SECURITY;

-- Row Level Security Policies (example - customize based on your auth setup)
-- CREATE POLICY "Users can view their own data" ON users FOR SELECT USING (auth.uid() = id);
-- CREATE POLICY "Students can view all jobs" ON jobs FOR SELECT TO authenticated USING (true);
-- CREATE POLICY "Students can manage their own saved jobs" ON saved_jobs FOR ALL USING (auth.uid() = user_id);

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'TradeG8 database schema created successfully!';
    RAISE NOTICE 'Tables created: users, jobs, saved_jobs, resumes, activity_logs, case_notes, compliance_reports, companies';
    RAISE NOTICE 'Indexes and triggers applied.';
    RAISE NOTICE 'Ready to use!';
END $$;
