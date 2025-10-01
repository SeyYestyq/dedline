import { useEffect, useState } from 'react';
import WebApp from '@twa-dev/sdk';
import './App.css';

// Fallback ID для локального запуска
const FALLBACK_TG_ID = 123456789;

function App() {
    const [tasks, setTasks] = useState({
        urgent: [],
        current: [],
        upcoming: []
    });
    const [subjects, setSubjects] = useState([]);
    const [userId, setUserId] = useState(null);

    useEffect(() => {
        WebApp.ready();
        WebApp.expand();
        
        const tgUser = WebApp.initDataUnsafe?.user;
        const id = tgUser?.id || FALLBACK_TG_ID; // fallback для локальной отладки
        
        setUserId(id);
        if (id) {
            loadTasks(id);
            loadSubjects(id);
        }
    }, []);

    const loadTasks = async (telegramId) => {
        try {
            console.log('Loading tasks for user:', telegramId);
            const response = await fetch(`http://localhost:8000/api/tasks/${telegramId}`);
            console.log('Tasks response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Tasks data:', data);
            setTasks(data);
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    };

    const loadSubjects = async (telegramId) => {
        try {
            console.log('Loading subjects for user:', telegramId);
            const response = await fetch(`http://localhost:8000/api/subjects/${telegramId}`);
            console.log('Subjects response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Subjects data:', data);
            setSubjects(data.subjects);
        } catch (error) {
            console.error('Error loading subjects:', error);
        }
    };

    const completeTask = async (taskId) => {
        await fetch(`http://localhost:8000/api/tasks/${taskId}/complete`, {
            method: 'PATCH'
        });
        loadTasks(userId);
        loadSubjects(userId);
    };

    const TaskCard = ({ task }) => {
        const formatDate = (date) => {
            return new Date(date).toLocaleDateString('ru-RU', {
                day: 'numeric',
                month: 'long'
            });
        };

        const getUrgencyColor = () => {
            if (task.urgency === 'overdue') return '#ff0000';
            if (task.urgency === 'urgent') return '#ff6b6b';
            return '#666';
        };

  return (
            <div className="task-card" style={{ borderLeftColor: getUrgencyColor() }}>
                <div className="task-header">
                    <h4>{task.subject}</h4>
                    <span className="points">{task.points ? `${task.points} б.` : ''}</span>
                </div>
                
                <div className="task-info">
                    <p className="task-name">{task.formatted_name}</p>
                    {task.description && (
                        <p className="task-description">{task.description}</p>
                    )}
                </div>

                <div className="task-footer">
                    <div className="deadline-info">
                        <span className="date">
                            📅 {formatDate(task.deadline_start)} — {formatDate(task.deadline_end)}
                        </span>
                        <span className={`days-left ${task.urgency}`}>
                            {task.days_left >= 0 
                                ? `Осталось ${task.days_left} дн.` 
                                : `Просрочено на ${Math.abs(task.days_left)} дн.`}
                        </span>
      </div>
                    
                    <button 
                        className="complete-btn"
                        onClick={() => completeTask(task.id)}
                    >
                        ✅ Выполнено
        </button>
                </div>

                {task.first_reminder && (
                    <div className="reminders">
                        <small>
                            🔔 Напоминания: {formatDate(task.first_reminder)} и {formatDate(task.second_reminder)}
                        </small>
                    </div>
                )}
            </div>
        );
    };

    const SubjectCard = ({ subject }) => {
        const progress = subject.total_tasks > 0 
            ? (subject.completed / subject.total_tasks * 100).toFixed(0) 
            : 0;

        return (
            <div className="subject-card">
                <h4>{subject.subject}</h4>
                <div className="subject-stats">
                    <div className="stat">
                        <span className="stat-value">{subject.pending}</span>
                        <span className="stat-label">Осталось</span>
                    </div>
                    <div className="stat">
                        <span className="stat-value">{subject.completed}</span>
                        <span className="stat-label">Выполнено</span>
                    </div>
                    <div className="stat">
                        <span className="stat-value">{subject.total_points || 0}</span>
                        <span className="stat-label">Баллов</span>
                    </div>
                </div>
                
                <div className="progress-bar">
                    <div 
                        className="progress-fill" 
                        style={{ width: `${progress}%` }}
                    />
                </div>
                <p className="progress-text">{progress}% выполнено</p>
                
                {subject.nearest_deadline && (
                    <p className="next-deadline">
                        Ближайший дедлайн: {new Date(subject.nearest_deadline).toLocaleDateString('ru-RU')}
                    </p>
                )}
            </div>
        );
    };

    return (
        <div className="app">
            {/* СТАТИСТИКА ПО ПРЕДМЕТАМ */}
            {subjects.length > 0 && (
                <section className="subjects-section">
                    <h2>📚 Статистика по предметам</h2>
                    <div className="subjects-grid">
                        {subjects.map((subject, index) => (
                            <SubjectCard key={index} subject={subject} />
                        ))}
                    </div>
                </section>
            )}

            <div className="tasks-view">
                {/* СРОЧНЫЕ ЗАДАЧИ */}
                <section className="section urgent-section">
                    <div className="section-header">
                        <h2>🔥 Срочно</h2>
                        <span className="badge">{tasks.urgent.length}</span>
                    </div>
                    {tasks.urgent.length === 0 ? (
                        <p className="empty-state">🎉 Срочных задач нет!</p>
                    ) : (
                        <div className="tasks-list">
                            {tasks.urgent.map(task => (
                                <TaskCard key={task.id} task={task} />
                            ))}
                        </div>
                    )}
                </section>

                {/* ТЕКУЩИЕ ЗАДАЧИ */}
                <section className="section current-section">
                    <div className="section-header">
                        <h2>⏰ Текущие</h2>
                        <span className="badge">{tasks.current.length}</span>
                    </div>
                    {tasks.current.length === 0 ? (
                        <p className="empty-state">Текущих задач нет</p>
                    ) : (
                        <div className="tasks-list">
                            {tasks.current.map(task => (
                                <TaskCard key={task.id} task={task} />
                            ))}
                        </div>
                    )}
                </section>

                {/* БУДУЩИЕ ЗАДАЧИ */}
                <section className="section upcoming-section">
                    <div className="section-header">
                        <h2>📅 Скоро</h2>
                        <span className="badge">{tasks.upcoming.length}</span>
                    </div>
                    {tasks.upcoming.length === 0 ? (
                        <p className="empty-state">Будущих задач нет</p>
                    ) : (
                        <div className="tasks-list">
                            {tasks.upcoming.map(task => (
                                <TaskCard key={task.id} task={task} />
                            ))}
                        </div>
                    )}
                </section>
            </div>
      </div>
    );
}

export default App;