const API_BASE_URL = 'http://localhost:8000/api';

class ResumeApp {
    constructor() {
        this.initializeEventListeners();
        this.loadResumeHistory();
    }

    initializeEventListeners() {
        // File input change
        document.getElementById('fileInput').addEventListener('change', (e) => {
            this.handleFileUpload(e.target.files[0]);
        });

        // Drag and drop
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileUpload(files[0]);
            }
        });

        // Tab change event
        document.getElementById('history-tab').addEventListener('shown.bs.tab', () => {
            this.loadResumeHistory();
        });
    }

    async handleFileUpload(file) {
        if (!file) return;

        // Validate file type
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
        if (!allowedTypes.includes(file.type)) {
            this.showAlert('Please select a PDF or DOCX file.', 'danger');
            return;
        }

        // Show progress
        this.showProgress(true);
        this.hideResults();

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_BASE_URL}/upload_resume`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const data = await response.json();
            this.displayResults(data);
            this.showAlert('Resume uploaded and analyzed successfully!', 'success');

        } catch (error) {
            console.error('Upload error:', error);
            this.showAlert(`Error: ${error.message}`, 'danger');
        } finally {
            this.showProgress(false);
        }
    }

    showProgress(show) {
        const progressDiv = document.getElementById('uploadProgress');
        if (show) {
            progressDiv.style.display = 'block';
            progressDiv.querySelector('.progress-bar').style.width = '100%';
        } else {
            progressDiv.style.display = 'none';
            progressDiv.querySelector('.progress-bar').style.width = '0%';
        }
    }

    hideResults() {
        document.getElementById('resultsSection').style.display = 'none';
    }

    displayResults(data) {
        // Personal Information
        document.getElementById('personalInfo').innerHTML = `
            <p><strong>Name:</strong> ${data.name || 'Not provided'}</p>
            <p><strong>Email:</strong> ${data.email || 'Not provided'}</p>
            <p><strong>Phone:</strong> ${data.phone || 'Not provided'}</p>
            <p><strong>LinkedIn:</strong> ${data.linkedin || 'Not provided'}</p>
            <p><strong>GitHub:</strong> ${data.github || 'Not provided'}</p>
            <p><strong>Address:</strong> ${data.address || 'Not provided'}</p>
        `;

        // AI Analysis
        document.getElementById('aiAnalysis').innerHTML = `
            <div class="mb-3">
                <strong>Rating:</strong> 
                <span class="badge bg-primary rating-badge">${data.resume_rating || 'N/A'}</span>
            </div>
            <div class="mb-3">
                <strong>Improvement Areas:</strong>
                ${data.improvement_areas?.length ? 
                    data.improvement_areas.map(area => `<div class="improvement-item">${area}</div>`).join('') : 
                    '<p class="text-muted">No specific areas identified</p>'
                }
            </div>
            <div>
                <strong>Upskill Suggestions:</strong>
                ${data.upskill_suggestions?.length ? 
                    data.upskill_suggestions.map(skill => `<div class="upskill-item">${skill}</div>`).join('') : 
                    '<p class="text-muted">No suggestions available</p>'
                }
            </div>
        `;

        // Skills
        document.getElementById('skillsInfo').innerHTML = `
            <div class="mb-3">
                <strong>Core Skills:</strong>
                <div class="mt-2">
                    ${data.core_skills?.length ? 
                        data.core_skills.map(skill => `<span class="skill-badge">${skill}</span>`).join('') : 
                        '<p class="text-muted">No core skills listed</p>'
                    }
                </div>
            </div>
            <div>
                <strong>Soft Skills:</strong>
                <div class="mt-2">
                    ${data.soft_skills?.length ? 
                        data.soft_skills.map(skill => `<span class="skill-badge">${skill}</span>`).join('') : 
                        '<p class="text-muted">No soft skills listed</p>'
                    }
                </div>
            </div>
        `;

        // Education
        document.getElementById('educationInfo').innerHTML = data.education?.length ? 
            data.education.map(edu => `
                <div class="mb-3">
                    <strong>${edu.degree || 'Degree not specified'}</strong>
                    <br><em>${edu.institution || 'Institution not specified'}</em>
                    ${edu.year ? `<br>Year: ${edu.year}` : ''}
                    ${edu.gpa ? `<br>GPA: ${edu.gpa}` : ''}
                </div>
            `).join('') : '<p class="text-muted">No education information available</p>';

        // Work Experience
        document.getElementById('experienceInfo').innerHTML = data.work_experience?.length ? 
            data.work_experience.map(exp => `
                <div class="experience-item">
                    <h6>${exp.position || 'Position not specified'}</h6>
                    <p class="text-muted mb-2">${exp.company || 'Company not specified'} | ${exp.duration || 'Duration not specified'}</p>
                    <p>${exp.description || 'No description available'}</p>
                </div>
            `).join('') : '<p class="text-muted">No work experience information available</p>';

        // Projects
        document.getElementById('projectsInfo').innerHTML = data.projects?.length ? 
            data.projects.map(project => `
                <div class="project-item">
                    <h6>${project.name || 'Project name not specified'}</h6>
                    <p>${project.description || 'No description available'}</p>
                    ${project.technologies_used?.length ? 
                        `<div><strong>Technologies:</strong> ${project.technologies_used.join(', ')}</div>` : 
                        ''
                    }
                </div>
            `).join('') : '<p class="text-muted">No projects information available</p>';

        // Show results
        document.getElementById('resultsSection').style.display = 'block';
    }

    async loadResumeHistory() {
        try {
            const response = await fetch(`${API_BASE_URL}/resumes`);
            if (!response.ok) throw new Error('Failed to load resume history');

            const resumes = await response.json();
            this.displayResumeHistory(resumes);

        } catch (error) {
            console.error('Error loading resume history:', error);
            document.getElementById('historyTableBody').innerHTML = 
                '<tr><td colspan="6" class="text-center text-muted">Error loading resume history</td></tr>';
        }
    }

    displayResumeHistory(resumes) {
        const tbody = document.getElementById('historyTableBody');
        
        if (resumes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No resumes uploaded yet</td></tr>';
            return;
        }

        tbody.innerHTML = resumes.map(resume => `
            <tr>
                <td>${resume.name || 'Unknown'}</td>
                <td>${resume.email || 'Unknown'}</td>
                <td>${resume.phone || 'Unknown'}</td>
                <td>${resume.file_name}</td>
                <td>${new Date(resume.upload_date).toLocaleDateString()}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-2" onclick="app.viewResumeDetails(${resume.id})">
                        <i class="fas fa-eye"></i> Details
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="app.deleteResume(${resume.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            </tr>
        `).join('');
    }

    async viewResumeDetails(resumeId) {
        try {
            const response = await fetch(`${API_BASE_URL}/resume/${resumeId}`);
            if (!response.ok) throw new Error('Failed to load resume details');

            const resume = await response.json();
            this.displayResumeModal(resume);

        } catch (error) {
            console.error('Error loading resume details:', error);
            this.showAlert('Error loading resume details', 'danger');
        }
    }

    displayResumeModal(data) {
        const modalContent = document.getElementById('modalContent');
        modalContent.innerHTML = `
            <div class="row">
                <!-- Personal Information -->
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header bg-info text-white">
                            <h6 class="mb-0"><i class="fas fa-user me-2"></i>Personal Information</h6>
                        </div>
                        <div class="card-body">
                            <p><strong>Name:</strong> ${data.name || 'Not provided'}</p>
                            <p><strong>Email:</strong> ${data.email || 'Not provided'}</p>
                            <p><strong>Phone:</strong> ${data.phone || 'Not provided'}</p>
                            <p><strong>LinkedIn:</strong> ${data.linkedin || 'Not provided'}</p>
                            <p><strong>GitHub:</strong> ${data.github || 'Not provided'}</p>
                            <p><strong>Address:</strong> ${data.address || 'Not provided'}</p>
                        </div>
                    </div>
                </div>

                <!-- AI Analysis -->
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header bg-warning text-dark">
                            <h6 class="mb-0"><i class="fas fa-robot me-2"></i>AI Analysis</h6>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <strong>Rating:</strong> 
                                <span class="badge bg-primary rating-badge">${data.resume_rating || 'N/A'}</span>
                            </div>
                            <div class="mb-3">
                                <strong>Improvement Areas:</strong>
                                ${data.improvement_areas?.length ? 
                                    data.improvement_areas.map(area => `<div class="improvement-item">${area}</div>`).join('') : 
                                    '<p class="text-muted">No specific areas identified</p>'
                                }
                            </div>
                            <div>
                                <strong>Upskill Suggestions:</strong>
                                ${data.upskill_suggestions?.length ? 
                                    data.upskill_suggestions.map(skill => `<div class="upskill-item">${skill}</div>`).join('') : 
                                    '<p class="text-muted">No suggestions available</p>'
                                }
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Skills -->
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header bg-success text-white">
                            <h6 class="mb-0"><i class="fas fa-tools me-2"></i>Skills</h6>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <strong>Core Skills:</strong>
                                <div class="mt-2">
                                    ${data.core_skills?.length ? 
                                        data.core_skills.map(skill => `<span class="skill-badge">${skill}</span>`).join('') : 
                                        '<p class="text-muted">No core skills listed</p>'
                                    }
                                </div>
                            </div>
                            <div>
                                <strong>Soft Skills:</strong>
                                <div class="mt-2">
                                    ${data.soft_skills?.length ? 
                                        data.soft_skills.map(skill => `<span class="skill-badge">${skill}</span>`).join('') : 
                                        '<p class="text-muted">No soft skills listed</p>'
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Education -->
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header bg-primary text-white">
                            <h6 class="mb-0"><i class="fas fa-graduation-cap me-2"></i>Education</h6>
                        </div>
                        <div class="card-body">
                            ${data.education?.length ? 
                                data.education.map(edu => `
                                    <div class="mb-3">
                                        <strong>${edu.degree || 'Degree not specified'}</strong>
                                        <br><em>${edu.institution || 'Institution not specified'}</em>
                                        ${edu.year ? `<br>Year: ${edu.year}` : ''}
                                        ${edu.gpa ? `<br>GPA: ${edu.gpa}` : ''}
                                    </div>
                                `).join('') : '<p class="text-muted">No education information available</p>'
                            }
                        </div>
                    </div>
                </div>

                <!-- Work Experience -->
                <div class="col-12 mb-4">
                    <div class="card">
                        <div class="card-header bg-secondary text-white">
                            <h6 class="mb-0"><i class="fas fa-briefcase me-2"></i>Work Experience</h6>
                        </div>
                        <div class="card-body">
                            ${data.work_experience?.length ? 
                                data.work_experience.map(exp => `
                                    <div class="experience-item">
                                        <h6>${exp.position || 'Position not specified'}</h6>
                                        <p class="text-muted mb-2">${exp.company || 'Company not specified'} | ${exp.duration || 'Duration not specified'}</p>
                                        <p>${exp.description || 'No description available'}</p>
                                    </div>
                                `).join('') : '<p class="text-muted">No work experience information available</p>'
                            }
                        </div>
                    </div>
                </div>

                <!-- Projects -->
                <div class="col-12 mb-4">
                    <div class="card">
                        <div class="card-header bg-dark text-white">
                            <h6 class="mb-0"><i class="fas fa-project-diagram me-2"></i>Projects</h6>
                        </div>
                        <div class="card-body">
                            ${data.projects?.length ? 
                                data.projects.map(project => `
                                    <div class="project-item">
                                        <h6>${project.name || 'Project name not specified'}</h6>
                                        <p>${project.description || 'No description available'}</p>
                                        ${project.technologies_used?.length ? 
                                            `<div><strong>Technologies:</strong> ${project.technologies_used.join(', ')}</div>` : 
                                            ''
                                        }
                                    </div>
                                `).join('') : '<p class="text-muted">No projects information available</p>'
                            }
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
        modal.show();
    }

    async deleteResume(resumeId) {
        if (!confirm('Are you sure you want to delete this resume?')) return;

        try {
            const response = await fetch(`${API_BASE_URL}/resume/${resumeId}`, {
                method: 'DELETE'
            });

            if (!response.ok) throw new Error('Failed to delete resume');

            this.showAlert('Resume deleted successfully', 'success');
            this.loadResumeHistory();

        } catch (error) {
            console.error('Error deleting resume:', error);
            this.showAlert('Error deleting resume', 'danger');
        }
    }

    showAlert(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at top of container
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);

        // Auto dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ResumeApp();
});
