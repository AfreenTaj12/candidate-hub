
import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [search, setSearch] = useState('');
  const [location, setLocation] = useState('');
  const [jobType, setJobType] = useState('');

  const [showRegister, setShowRegister] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [token, setToken] = useState('');
  const [authMessage, setAuthMessage] = useState('');

  const [profile, setProfile] = useState(null);
  const [editName, setEditName] = useState('');

  const [applicationMessage, setApplicationMessage] = useState('');
  const [applications, setApplications] = useState([]);

  // Registration and Login
  const handleAuth = async () => {
    const endpoint = showRegister
      ? 'http://127.0.0.1:8000/auth/register'
      : 'http://127.0.0.1:8000/auth/login';

    const userData = showRegister
      ? { name, email, password }
      : { email, password };

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      if (showRegister) {
        setAuthMessage('Registration successful! Please log in.');
        setShowRegister(false);
        setPassword('');
      } else {
        setToken(data.access_token);

        const profileResponse = await fetch(
          'http://127.0.0.1:8000/candidates/me',
          {
            headers: {
              Authorization: `Bearer ${data.access_token}`,
            },
          }
        );

        if (!profileResponse.ok) {
          throw new Error('Unable to load candidate profile');
        }

        const profileData = await profileResponse.json();

        setProfile(profileData);
        setEditName(profileData.name);
        setAuthMessage('Login successful!');
        setPassword('');
      }
    } catch (error) {
      setAuthMessage(error.message);
    }
  };

  // Update Candidate Profile
  const handleUpdateProfile = async () => {
    try {
      const response = await fetch(
        'http://127.0.0.1:8000/candidates/me',
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ name: editName }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Profile update failed');
      }

      setProfile(data);
      setAuthMessage('Profile updated successfully!');
    } catch (error) {
      setAuthMessage(error.message);
    }
  };

  // Apply for a Job
  const handleApply = async (jobId) => {
    if (!token) {
      setApplicationMessage('Please log in before applying.');
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/applications/${jobId}`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Application failed');
      }

      setApplicationMessage('Application submitted successfully!');
    } catch (error) {
      setApplicationMessage(error.message);
    }
  };

  // View My Applications
  const handleViewApplications = async () => {
    if (!token) {
      setApplicationMessage('Please log in first.');
      return;
    }

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/applications/me',
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Unable to load applications');
      }

      setApplications(data);
      setApplicationMessage('');
    } catch (error) {
      setApplicationMessage(error.message);
    }
  };

  // Fetch Jobs from FastAPI
  useEffect(() => {
    setLoading(true);
    setError('');

    fetch(
      `http://127.0.0.1:8000/jobs/?search=${encodeURIComponent(search)}&location=${encodeURIComponent(location)}&job_type=${encodeURIComponent(jobType)}`
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch jobs');
        }

        return response.json();
      })
      .then((data) => {
        setJobs(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Unable to load jobs. Please try again.');
        setLoading(false);
      });
  }, [search, location, jobType]);

  return (
    <div>
      {/* Navigation */}
      <header className="navbar">
        <h2>CandidateHub</h2>

        <nav>
          <a href="#home">Home</a>
          <a href="#jobs">Browse Jobs</a>
          <a href="#login">Login</a>
          <a href="#applications">My Applications</a>
        </nav>
      </header>

      {/* Authentication */}
      <section className="auth-section" id="login">
        <h2>
          {showRegister ? 'Create Account' : 'Candidate Login'}
        </h2>

        {showRegister && (
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        )}

        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="button" onClick={handleAuth}>
          {showRegister ? 'Register' : 'Login'}
        </button>

        {authMessage && <p>{authMessage}</p>}

        {profile && (
          <div>
            <h3>Welcome, {profile.name}!</h3>
            <p>Email: {profile.email}</p>

            <input
              type="text"
              placeholder="Update your name"
              value={editName}
              onChange={(e) => setEditName(e.target.value)}
            />

            <button
              type="button"
              onClick={handleUpdateProfile}
            >
              Update Profile
            </button>
          </div>
        )}

        <p>
          {showRegister
            ? 'Already have an account?'
            : "Don't have an account?"}

          <button
            type="button"
            onClick={() => {
              setShowRegister(!showRegister);
              setAuthMessage('');
            }}
          >
            {showRegister ? 'Login' : 'Register'}
          </button>
        </p>
      </section>

      {/* Homepage */}
      <section className="hero" id="home">
        <h1>Find Your Dream Job</h1>

        <p>
          Discover opportunities, apply for jobs,
          and track your applications in one place.
        </p>

        <a href="#jobs" className="primary-button">
          Explore Jobs
        </a>
      </section>

      {/* Job Listings */}
      <section className="jobs-section" id="jobs">
        <h2>Available Jobs</h2>

        <input
          type="text"
          placeholder="Search jobs by title..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <input
          type="text"
          placeholder="Filter by location..."
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />

        <select
          value={jobType}
          onChange={(e) => setJobType(e.target.value)}
        >
          <option value="">All Job Types</option>
          <option value="Internship">Internship</option>
          <option value="Full-time">Full-time</option>
        </select>

        {loading && <p>Loading jobs...</p>}

        {error && <p>{error}</p>}

        {!loading && !error && jobs.length === 0 && (
          <p>No jobs available.</p>
        )}

        {jobs.map((job) => (
          <div className="job-card" key={job.id}>
            <h3>{job.title}</h3>
            <p>{job.company}</p>
            <p>{job.location} · {job.job_type}</p>
            <p>{job.description}</p>

            <button
              type="button"
              onClick={() => handleApply(job.id)}
            >
              Apply Now
            </button>
          </div>
        ))}

        {applicationMessage && <p>{applicationMessage}</p>}
      </section>

      {/* My Applications */}
      <section className="jobs-section" id="applications">
        <h2>My Applications</h2>

        <button
          type="button"
          onClick={handleViewApplications}
        >
          View My Applications
        </button>

        {applications.map((application) => (
          <div className="job-card" key={application.id}>
            <h3>Job ID: {application.job_id}</h3>
            <p>Status: {application.status}</p>
            <p>
              Applied on:{' '}
              {application.applied_at
                ? new Date(application.applied_at).toLocaleDateString()
                : 'Date unavailable'}
            </p>
          </div>
        ))}

        {applications.length === 0 && (
          <p>No applications found. Log in and click View My Applications.</p>
        )}
      </section>
    </div>
  );
}

export default App;
