/**
 * TACTIK AI MVP - Frontend JavaScript
 * Handles UI interactions and API communication
 */

const API_BASE = window.location.origin;
let currentSession = null;
let sourceCounter = 0;

// ═══════════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    showTab('avatars');
    loadAvatars();
});

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        document.getElementById('health-status').textContent = `✓ ${data.status} (${data.avatars_loaded} avatars)`;
    } catch (error) {
        document.getElementById('health-status').textContent = '✗ Offline';
    }
}

// ═══════════════════════════════════════════════════════════════════
// TAB NAVIGATION
// ═══════════════════════════════════════════════════════════════════

function showTab(tabName) {
    // Hide all content
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));

    // Remove active from all tabs
    document.querySelectorAll('.tab-btn').forEach(el => {
        el.classList.remove('border-purple-600', 'text-purple-600');
        el.classList.add('border-transparent', 'text-gray-700');
    });

    // Show selected content
    document.getElementById(`content-${tabName}`).classList.remove('hidden');

    // Activate tab
    const activeTab = document.getElementById(`tab-${tabName}`);
    activeTab.classList.remove('border-transparent', 'text-gray-700');
    activeTab.classList.add('border-purple-600', 'text-purple-600');

    // Load data for tab
    if (tabName === 'avatars') {
        loadAvatars();
    } else if (tabName === 'sessions') {
        loadSessions();
    }
}

// ═══════════════════════════════════════════════════════════════════
// AVATARS
// ═══════════════════════════════════════════════════════════════════

async function loadAvatars() {
    try {
        const response = await fetch(`${API_BASE}/api/avatars`);
        const data = await response.json();

        const container = document.getElementById('avatars-list');
        const noAvatars = document.getElementById('no-avatars');

        if (data.avatars.length === 0) {
            container.innerHTML = '';
            noAvatars.classList.remove('hidden');
        } else {
            noAvatars.classList.add('hidden');
            container.innerHTML = data.avatars.map(avatar => createAvatarCard(avatar)).join('');
        }
    } catch (error) {
        console.error('Error loading avatars:', error);
    }
}

function createAvatarCard(avatar) {
    const fidelityColor = avatar.avda_score >= 75 ? 'green' : avatar.avda_score >= 60 ? 'yellow' : 'red';

    return `
        <div class="card bg-white rounded-lg shadow-lg p-6">
            <div class="flex items-start justify-between mb-4">
                <div>
                    <h3 class="text-lg font-bold text-gray-800">${avatar.avatar_name}</h3>
                    <p class="text-sm text-gray-600">${avatar.role}</p>
                </div>
                <div class="text-right">
                    <div class="text-2xl font-bold text-${fidelityColor}-600">${avatar.avda_score}%</div>
                    <div class="text-xs text-gray-500">AVDA Score</div>
                </div>
            </div>

            <div class="space-y-2 mb-4 text-sm">
                <div class="flex justify-between">
                    <span class="text-gray-600">Sources:</span>
                    <span class="font-semibold">${avatar.sources_count}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-600">Coverage:</span>
                    <span class="font-semibold">${avatar.source_coverage}%</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-600">Classification:</span>
                    <span class="font-semibold text-${fidelityColor}-600">${avatar.classification}</span>
                </div>
            </div>

            <button onclick="viewAvatar('${avatar.avatar_id}')" class="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm font-semibold">
                View Details
            </button>
        </div>
    `;
}

async function viewAvatar(avatarId) {
    try {
        const response = await fetch(`${API_BASE}/api/avatars/${avatarId}`);
        const data = await response.json();

        alert(`Avatar: ${data.avatar_name}\n\nAVDA Score: ${data.avda_metrics.avda_score}%\nClassification: ${data.avda_metrics.classification}\n\nRecommendation:\n${data.recommendation}`);
    } catch (error) {
        console.error('Error viewing avatar:', error);
        alert('Error loading avatar details');
    }
}

// ═══════════════════════════════════════════════════════════════════
// CREATE AVATAR
// ═══════════════════════════════════════════════════════════════════

function addSource() {
    sourceCounter++;
    const container = document.getElementById('sources-container');

    const sourceHTML = `
        <div class="source-item p-4 bg-gray-50 rounded-lg" id="source-${sourceCounter}">
            <div class="flex justify-between items-start mb-3">
                <h4 class="font-semibold text-sm">Source ${sourceCounter}</h4>
                <button type="button" onclick="removeSource(${sourceCounter})" class="text-red-500 hover:text-red-700">✕</button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">Tier</label>
                    <select class="source-tier w-full px-3 py-2 border border-gray-300 rounded text-sm">
                        <option value="tier_1_primary">Tier 1 - Primary (100%)</option>
                        <option value="tier_2_secondary">Tier 2 - Secondary (85%)</option>
                        <option value="tier_3_tertiary">Tier 3 - Tertiary (60%)</option>
                        <option value="tier_4_inferred">Tier 4 - Inferred (40%)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">URL (optional)</label>
                    <input type="url" class="source-url w-full px-3 py-2 border border-gray-300 rounded text-sm" placeholder="https://...">
                </div>
            </div>

            <div class="mt-3">
                <label class="block text-xs font-medium text-gray-700 mb-1">Description</label>
                <input type="text" class="source-description w-full px-3 py-2 border border-gray-300 rounded text-sm" placeholder="Brief description of source" required>
            </div>

            <div class="mt-3 flex items-center">
                <input type="checkbox" class="source-verified mr-2" id="verified-${sourceCounter}">
                <label for="verified-${sourceCounter}" class="text-xs text-gray-700">Cross-verified</label>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', sourceHTML);
}

function removeSource(id) {
    document.getElementById(`source-${id}`).remove();
}

async function createAvatar(event) {
    event.preventDefault();

    // Collect basic info
    const avatarData = {
        avatar_id: document.getElementById('avatar_id').value,
        avatar_name: document.getElementById('avatar_name').value,
        role: document.getElementById('role').value,
        environment: document.getElementById('environment').value,
        language: document.getElementById('language').value,
        sources: [],
        constraints: {}
    };

    // Collect sources
    document.querySelectorAll('.source-item').forEach((item, index) => {
        const tier = item.querySelector('.source-tier').value;
        const url = item.querySelector('.source-url').value;
        const description = item.querySelector('.source-description').value;
        const verified = item.querySelector('.source-verified').checked;

        avatarData.sources.push({
            source_id: `${avatarData.avatar_id}_${index + 1}`,
            tier: tier,
            description: description,
            url: url || null,
            date: new Date().toISOString().split('T')[0],
            cross_verified: verified
        });
    });

    // Parse simplified DNA (for MVP)
    const influences = document.getElementById('influences').value.split(',').map(s => s.trim()).filter(Boolean);
    const behaviors = document.getElementById('behaviors').value.split(',').map(s => s.trim()).filter(Boolean);
    const communication = document.getElementById('communication').value;
    const priorities = document.getElementById('priorities').value.split(',').map(s => s.trim()).filter(Boolean);

    // Build verified components (simplified for MVP)
    avatarData.influences_verified = influences.map((inf, i) => ({
        influence: inf,
        source_id: avatarData.sources[Math.min(i, avatarData.sources.length - 1)]?.source_id || avatarData.sources[0]?.source_id,
        impact: "medium"
    }));
    avatarData.influences_inferred = [];

    avatarData.thoughts_verified = influences.slice(0, 3).map((inf, i) => ({
        thought: `Strategic thinking about ${inf.toLowerCase()}`,
        source_id: avatarData.sources[Math.min(i, avatarData.sources.length - 1)]?.source_id || avatarData.sources[0]?.source_id
    }));
    avatarData.thoughts_inferred = [];

    avatarData.behavioral_verified = behaviors.map((beh, i) => ({
        behavior: beh,
        source_id: avatarData.sources[Math.min(i, avatarData.sources.length - 1)]?.source_id || avatarData.sources[0]?.source_id,
        context: "Documented pattern"
    }));
    avatarData.behavioral_inferred = [];

    avatarData.decision_style_verified = [{
        style: behaviors[0] || "Strategic decision-making",
        source_id: avatarData.sources[0]?.source_id
    }];
    avatarData.decision_style_inferred = [];

    avatarData.communication_verified = [{
        style: communication,
        source_id: avatarData.sources[0]?.source_id
    }];
    avatarData.communication_inferred = [];

    avatarData.priorities_verified = priorities.map((pri, i) => ({
        priority: `${i + 1}. ${pri}`,
        source_id: avatarData.sources[Math.min(i, avatarData.sources.length - 1)]?.source_id || avatarData.sources[0]?.source_id
    }));
    avatarData.priorities_inferred = [];

    try {
        const response = await fetch(`${API_BASE}/api/avatars`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(avatarData)
        });

        const result = await response.json();

        if (result.success) {
            alert(`✓ Avatar created successfully!\n\nAVDA Score: ${result.avda_score.avda_score}%\nSource Coverage: ${result.source_coverage}%`);
            resetAvatarForm();
            showTab('avatars');
        } else {
            alert('Error creating avatar: ' + (result.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error creating avatar:', error);
        alert('Error creating avatar. Check console for details.');
    }
}

function resetAvatarForm() {
    document.getElementById('avatar-form').reset();
    document.getElementById('sources-container').innerHTML = '';
    sourceCounter = 0;
}

// ═══════════════════════════════════════════════════════════════════
// SESSIONS
// ═══════════════════════════════════════════════════════════════════

async function loadSessions() {
    try {
        const response = await fetch(`${API_BASE}/api/sessions`);
        const data = await response.json();

        const container = document.getElementById('sessions-list');

        if (data.sessions.length === 0) {
            container.innerHTML = '<div class="text-center py-12 text-gray-500">No sessions yet. Create one to start!</div>';
        } else {
            container.innerHTML = data.sessions.map(session => createSessionCard(session)).join('');
        }
    } catch (error) {
        console.error('Error loading sessions:', error);
    }
}

function createSessionCard(session) {
    return `
        <div class="card bg-white rounded-lg shadow-lg p-6">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h3 class="text-lg font-bold text-gray-800">${session.user_goal}</h3>
                    <p class="text-sm text-gray-600 mt-1">Session: ${session.session_id}</p>
                </div>
                <div class="text-right">
                    <div class="text-2xl font-bold text-purple-600">${session.tactik_score || '-'}</div>
                    <div class="text-xs text-gray-500">TACTIK Score</div>
                </div>
            </div>

            <div class="text-sm text-gray-700 mb-4">
                <span class="font-semibold">${session.total_turns}</span> turns with
                <span class="font-semibold">${session.active_avatars.length}</span> avatar(s)
            </div>

            <div class="flex space-x-3">
                <button onclick="openConversation('${session.session_id}')" class="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm font-semibold">
                    Continue
                </button>
                <button onclick="viewSessionReport('${session.session_id}')" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm">
                    Report
                </button>
            </div>
        </div>
    `;
}

async function showCreateSession() {
    try {
        const response = await fetch(`${API_BASE}/api/avatars`);
        const data = await response.json();

        if (data.avatars.length === 0) {
            alert('Please create at least one avatar first!');
            showTab('create-avatar');
            return;
        }

        const avatarOptions = data.avatars.map(a => `<option value="${a.avatar_id}">${a.avatar_name}</option>`).join('');

        const goal = prompt('Enter your strategic goal for this session:');
        if (!goal) return;

        const selectedAvatar = prompt(`Select avatar ID:\n${data.avatars.map(a => `- ${a.avatar_id}: ${a.avatar_name}`).join('\n')}`);
        if (!selectedAvatar) return;

        const sessionId = `session_${Date.now()}`;

        const sessionData = {
            session_id: sessionId,
            user_goal: goal,
            avatar_ids: [selectedAvatar]
        };

        const createResponse = await fetch(`${API_BASE}/api/sessions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sessionData)
        });

        const result = await createResponse.json();

        if (result.success) {
            openConversation(sessionId);
        } else {
            alert('Error creating session: ' + (result.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error creating session:', error);
        alert('Error creating session');
    }
}

// ═══════════════════════════════════════════════════════════════════
// CONVERSATION
// ═══════════════════════════════════════════════════════════════════

async function openConversation(sessionId) {
    try {
        const response = await fetch(`${API_BASE}/api/sessions/${sessionId}`);
        const data = await response.json();

        currentSession = data;

        document.getElementById('modal-session-title').textContent = data.session_id;
        document.getElementById('modal-session-goal').textContent = data.user_goal;

        // Load transcript
        const messagesArea = document.getElementById('messages-area');
        messagesArea.innerHTML = data.transcript.map(turn => createMessageHTML(turn)).join('');

        // Update metrics
        updateMetrics(data.metrics);

        // Show modal
        document.getElementById('conversation-modal').classList.remove('hidden');

        // Scroll to bottom
        messagesArea.scrollTop = messagesArea.scrollHeight;
    } catch (error) {
        console.error('Error opening conversation:', error);
        alert('Error loading conversation');
    }
}

function closeConversation() {
    document.getElementById('conversation-modal').classList.add('hidden');
    currentSession = null;
    loadSessions();
}

function createMessageHTML(turn) {
    const isUser = turn.speaker_id === 'user';
    const className = isUser ? 'message-user' : 'message-avatar';

    return `
        <div class="flex ${isUser ? 'justify-end' : 'justify-start'}">
            <div class="${className} max-w-xl px-4 py-3">
                <div class="text-xs ${isUser ? 'text-gray-600' : 'text-white opacity-80'} mb-1">
                    ${turn.speaker_name}
                </div>
                <div class="text-sm">
                    ${turn.message}
                </div>
                ${!isUser ? `
                    <div class="mt-2 pt-2 border-t border-white border-opacity-20 text-xs opacity-70">
                        EIS: ${(turn.eis_score * 100).toFixed(0)}% | HCA: ${(turn.hca_score * 100).toFixed(0)}% | DNA: ${(turn.dna_score * 100).toFixed(0)}%
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

async function sendMessage(event) {
    event.preventDefault();

    const messageInput = document.getElementById('user-message');
    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message to UI
    const messagesArea = document.getElementById('messages-area');
    messagesArea.insertAdjacentHTML('beforeend', createMessageHTML({
        speaker_id: 'user',
        speaker_name: 'You',
        message: message
    }));

    messageInput.value = '';
    messagesArea.scrollTop = messagesArea.scrollHeight;

    // Send to API
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: currentSession.session_id,
                speaker_id: currentSession.active_avatars[0],
                message: message
            })
        });

        const result = await response.json();

        if (result.action === 'EMPATHY_PAUSE') {
            messagesArea.insertAdjacentHTML('beforeend', `
                <div class="text-center py-4">
                    <div class="inline-block bg-yellow-100 border border-yellow-300 rounded-lg px-4 py-3 text-sm">
                        ⚠️ <strong>Empathy Pause Activated</strong><br>
                        ${result.message}
                    </div>
                </div>
            `);
        } else if (result.action === 'TURN_COMPLETED') {
            messagesArea.insertAdjacentHTML('beforeend', createMessageHTML(result.turn));
            updateMetrics(result.session_metrics);

            if (result.backflow_triggered) {
                messagesArea.insertAdjacentHTML('beforeend', `
                    <div class="text-center py-2">
                        <div class="inline-block bg-blue-100 border border-blue-300 rounded-lg px-3 py-2 text-xs">
                            🔄 Backflow detected: ${result.backflow_issue} - Recalibrating
                        </div>
                    </div>
                `);
            }
        }

        messagesArea.scrollTop = messagesArea.scrollHeight;
    } catch (error) {
        console.error('Error sending message:', error);
        alert('Error sending message');
    }
}

function updateMetrics(metrics) {
    if (!metrics) return;

    document.getElementById('metric-turns').textContent = metrics.total_turns || 0;
    document.getElementById('metric-eis').textContent = metrics.avg_eis ? (metrics.avg_eis * 100).toFixed(0) + '%' : '-';
    document.getElementById('metric-hca').textContent = metrics.avg_hca ? (metrics.avg_hca * 100).toFixed(0) + '%' : '-';
    document.getElementById('metric-tactik').textContent = metrics.tactik_score ? metrics.tactik_score.toFixed(1) : '-';
}

// ═══════════════════════════════════════════════════════════════════
// REPORTS
// ═══════════════════════════════════════════════════════════════════

async function generateReport() {
    if (!currentSession) return;

    try {
        const response = await fetch(`${API_BASE}/api/sessions/${currentSession.session_id}/report`);
        const report = await response.json();

        let reportText = `TACTIK ADVISOR REPORT\n\n`;
        reportText += `Session: ${report.session_summary.session_id}\n`;
        reportText += `Goal: ${report.session_summary.goal}\n`;
        reportText += `TACTIK Score: ${report.session_summary.tactik_score}/10\n\n`;

        reportText += `KEY INSIGHTS:\n${report.key_insights.map(i => `• ${i}`).join('\n')}\n\n`;
        reportText += `RECOMMENDATIONS:\n${report.recommendations.map(r => `${r}`).join('\n')}\n\n`;

        alert(reportText);
    } catch (error) {
        console.error('Error generating report:', error);
        alert('Error generating report');
    }
}

async function exportPDF() {
    if (!currentSession) return;

    try {
        window.open(`${API_BASE}/api/sessions/${currentSession.session_id}/export/pdf`, '_blank');
    } catch (error) {
        console.error('Error exporting PDF:', error);
        alert('Error exporting PDF');
    }
}

async function viewSessionReport(sessionId) {
    try {
        const response = await fetch(`${API_BASE}/api/sessions/${sessionId}/report`);
        const report = await response.json();

        let reportText = `TACTIK ADVISOR REPORT\n\n`;
        reportText += `Session: ${report.session_summary.session_id}\n`;
        reportText += `TACTIK Score: ${report.session_summary.tactik_score}/10\n\n`;
        reportText += `KEY INSIGHTS:\n${report.key_insights.map(i => `• ${i}`).join('\n')}`;

        alert(reportText);
    } catch (error) {
        console.error('Error viewing report:', error);
        alert('Error loading report');
    }
}
