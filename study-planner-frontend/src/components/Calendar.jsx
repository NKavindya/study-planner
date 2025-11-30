import { useState, useMemo, useEffect, useCallback } from 'react';
import './Calendar.css';

const Calendar = ({ plan }) => {
  const [viewMode, setViewMode] = useState('weekly'); // 'daily', 'weekly', 'monthly'
  const [currentDate, setCurrentDate] = useState(new Date());
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);

  // Parse plan data and organize by date
  const planByDate = useMemo(() => {
    const organized = {};
    if (plan && Array.isArray(plan)) {
      plan.forEach(dayPlan => {
        const date = dayPlan.date || null;
        if (date) {
          if (!organized[date]) {
            organized[date] = {
              day: dayPlan.day,
              date: date,
              time_slots: []
            };
          }
          if (dayPlan.time_slots && Array.isArray(dayPlan.time_slots)) {
            organized[date].time_slots.push(...dayPlan.time_slots);
          }
        }
      });
    }
    return organized;
  }, [plan]);

  // Get all dates from plan
  const allDates = useMemo(() => {
    return Object.keys(planByDate).sort();
  }, [planByDate]);

  // Get current view dates based on view mode
  const getViewDates = () => {
    const dates = [];
    const start = new Date(currentDate);
    
    if (viewMode === 'daily') {
      dates.push(new Date(start));
    } else if (viewMode === 'weekly') {
      // Get Monday of current week
      const day = start.getDay();
      const diff = start.getDate() - day + (day === 0 ? -6 : 1); // Adjust to Monday
      const monday = new Date(start.setDate(diff));
      
      for (let i = 0; i < 7; i++) {
        const date = new Date(monday);
        date.setDate(monday.getDate() + i);
        dates.push(date);
      }
    } else if (viewMode === 'monthly') {
      // Get first day of month
      const firstDay = new Date(start.getFullYear(), start.getMonth(), 1);
      // Get last day of month
      const lastDay = new Date(start.getFullYear(), start.getMonth() + 1, 0);
      
      // Start from Monday of the week containing first day
      const firstDayOfWeek = firstDay.getDay();
      const startDate = new Date(firstDay);
      startDate.setDate(firstDay.getDate() - (firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1));
      
      // End on Sunday of the week containing last day
      const lastDayOfWeek = lastDay.getDay();
      const endDate = new Date(lastDay);
      endDate.setDate(lastDay.getDate() + (lastDayOfWeek === 0 ? 0 : 7 - lastDayOfWeek));
      
      const current = new Date(startDate);
      while (current <= endDate) {
        dates.push(new Date(current));
        current.setDate(current.getDate() + 1);
      }
    }
    
    return dates;
  };

  const viewDates = getViewDates();

  const formatDate = (date) => {
    return date.toISOString().split('T')[0];
  };

  const formatDateDisplay = (date) => {
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  const getDayName = (date) => {
    return date.toLocaleDateString('en-US', { weekday: 'long' });
  };

  const getPlanForDate = (dateStr) => {
    return planByDate[dateStr] || null;
  };

  const navigateDate = (direction) => {
    const newDate = new Date(currentDate);
    if (viewMode === 'daily') {
      newDate.setDate(newDate.getDate() + direction);
    } else if (viewMode === 'weekly') {
      newDate.setDate(newDate.getDate() + (direction * 7));
    } else if (viewMode === 'monthly') {
      newDate.setMonth(newDate.getMonth() + direction);
    }
    setCurrentDate(newDate);
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  const handleDateClick = (date) => {
    const dateStr = formatDate(date);
    const dayPlan = getPlanForDate(dateStr);
    if (dayPlan && dayPlan.time_slots && dayPlan.time_slots.length > 0) {
      setSelectedDate({ date, dateStr, dayPlan });
      setModalOpen(true);
    }
  };

  const closeModal = useCallback(() => {
    setModalOpen(false);
    setSelectedDate(null);
  }, []);

  // Close modal on ESC key
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && modalOpen) {
        closeModal();
      }
    };

    if (modalOpen) {
      window.addEventListener('keydown', handleKeyDown);
      return () => window.removeEventListener('keydown', handleKeyDown);
    }
  }, [modalOpen, closeModal]);

  const renderDailyView = () => {
    const dateStr = formatDate(currentDate);
    const dayPlan = getPlanForDate(dateStr);
    const timeSlots = dayPlan?.time_slots || [];

    return (
      <div className="calendar-daily-view">
        <div className="calendar-day-header">
          <h3>{getDayName(currentDate)}</h3>
          <p className="calendar-date">{formatDateDisplay(currentDate)}</p>
        </div>
        <div className="calendar-time-slots">
          {timeSlots.length === 0 ? (
            <div className="calendar-empty">No study sessions scheduled for this day</div>
          ) : (
            timeSlots.map((slot, idx) => (
              <div key={idx} className="calendar-slot">
                <div className="calendar-slot-time">{slot.time}</div>
                <div className="calendar-slot-content">
                  <div className="calendar-slot-title">{slot.item_name}</div>
                  <div className="calendar-slot-meta">
                    <span className={`badge badge-${slot.category}`}>{slot.category}</span>
                    <span className="calendar-slot-subject">{slot.subject_name}</span>
                    <span className="calendar-slot-hours">{slot.hours}h</span>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    );
  };

  const renderWeeklyView = () => {
    return (
      <div className="calendar-weekly-view">
        <div className="calendar-week-grid">
          {viewDates.map((date, idx) => {
            const dateStr = formatDate(date);
            const dayPlan = getPlanForDate(dateStr);
            const timeSlots = dayPlan?.time_slots || [];
            const isToday = formatDate(new Date()) === dateStr;

            return (
              <div key={idx} className={`calendar-week-day ${isToday ? 'today' : ''}`}>
                <div className="calendar-week-day-header">
                  <div className="calendar-week-day-name">{getDayName(date).substring(0, 3)}</div>
                  <div className={`calendar-week-day-number ${isToday ? 'today-number' : ''}`}>
                    {date.getDate()}
                  </div>
                </div>
                <div className="calendar-week-day-slots">
                  {timeSlots.slice(0, 3).map((slot, slotIdx) => (
                    <div key={slotIdx} className="calendar-week-slot">
                      <div className="calendar-week-slot-time">{slot.time}</div>
                      <div className="calendar-week-slot-name">{slot.item_name}</div>
                      <span className={`badge badge-${slot.category}`}>{slot.category}</span>
                    </div>
                  ))}
                  {timeSlots.length > 3 && (
                    <div className="calendar-week-more">+{timeSlots.length - 3} more</div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderMonthlyView = () => {
    const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    
    return (
      <div className="calendar-monthly-view">
        <div className="calendar-month-grid-header">
          {weekDays.map(day => (
            <div key={day} className="calendar-month-day-header">{day}</div>
          ))}
        </div>
        <div className="calendar-month-grid">
          {viewDates.map((date, idx) => {
            const dateStr = formatDate(date);
            const dayPlan = getPlanForDate(dateStr);
            const timeSlots = dayPlan?.time_slots || [];
            const isToday = formatDate(new Date()) === dateStr;
            const isCurrentMonth = date.getMonth() === currentDate.getMonth();

            return (
              <div 
                key={idx} 
                className={`calendar-month-day ${!isCurrentMonth ? 'other-month' : ''} ${isToday ? 'today' : ''} ${timeSlots.length > 0 ? 'has-plans' : ''}`}
                onClick={() => timeSlots.length > 0 && handleDateClick(date)}
                style={{ cursor: timeSlots.length > 0 ? 'pointer' : 'default' }}
              >
                <div className="calendar-month-day-number">{date.getDate()}</div>
                {timeSlots.length > 0 && (
                  <div className="calendar-month-day-indicator">
                    <div className="calendar-month-dot"></div>
                    <span className="calendar-month-count">{timeSlots.length}</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="calendar-container">
      <div className="calendar-controls">
        <div className="calendar-view-toggle">
          <button 
            className={viewMode === 'daily' ? 'active' : ''}
            onClick={() => setViewMode('daily')}
          >
            Daily
          </button>
          <button 
            className={viewMode === 'weekly' ? 'active' : ''}
            onClick={() => setViewMode('weekly')}
          >
            Weekly
          </button>
          <button 
            className={viewMode === 'monthly' ? 'active' : ''}
            onClick={() => setViewMode('monthly')}
          >
            Monthly
          </button>
        </div>
        <div className="calendar-navigation">
          <button onClick={() => navigateDate(-1)}>‹</button>
          <button onClick={goToToday}>Today</button>
          <button onClick={() => navigateDate(1)}>›</button>
        </div>
        <div className="calendar-title">
          {viewMode === 'daily' && formatDateDisplay(currentDate)}
          {viewMode === 'weekly' && `Week of ${formatDateDisplay(viewDates[0])}`}
          {viewMode === 'monthly' && currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
        </div>
      </div>

      <div className="calendar-content">
        {viewMode === 'daily' && renderDailyView()}
        {viewMode === 'weekly' && renderWeeklyView()}
        {viewMode === 'monthly' && renderMonthlyView()}
      </div>

      {/* Modal for showing daily plan details */}
      {modalOpen && selectedDate && (
        <div className="calendar-modal-overlay" onClick={closeModal}>
          <div className="calendar-modal" onClick={(e) => e.stopPropagation()}>
            <div className="calendar-modal-header">
              <h3>{getDayName(selectedDate.date)}</h3>
              <p className="calendar-modal-date">{formatDateDisplay(selectedDate.date)}</p>
              <button className="calendar-modal-close" onClick={closeModal}>×</button>
            </div>
            <div className="calendar-modal-content">
              {selectedDate.dayPlan.time_slots.length === 0 ? (
                <div className="calendar-empty">No study sessions scheduled for this day</div>
              ) : (
                selectedDate.dayPlan.time_slots.map((slot, idx) => (
                  <div key={idx} className="calendar-modal-slot">
                    <div className="calendar-modal-slot-time">{slot.time}</div>
                    <div className="calendar-modal-slot-content">
                      <div className="calendar-modal-slot-title">{slot.item_name}</div>
                      <div className="calendar-modal-slot-meta">
                        <span className={`badge badge-${slot.category}`}>{slot.category}</span>
                        <span className="calendar-modal-slot-subject">{slot.subject_name}</span>
                        <span className="calendar-modal-slot-hours">{slot.hours}h</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Calendar;

