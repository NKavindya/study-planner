import { formatDate } from '../utils/helpers';
import './StudyPlanTable.css';

const StudyPlanTable = ({ plan }) => {
  if (!plan || plan.length === 0) {
    return (
      <div className="no-plan">
        <p>No study plan generated yet. Generate a plan to see your schedule.</p>
      </div>
    );
  }

  return (
    <div className="study-plan-table">
      <h3>Weekly Study Plan</h3>
      <table className="table">
        <thead>
          <tr>
            <th>Day</th>
            <th>Time Slot</th>
            <th>Subject</th>
            <th>Hours</th>
          </tr>
        </thead>
        <tbody>
          {plan.map((dayPlan, idx) => (
            dayPlan.time_slots.map((slot, slotIdx) => (
              <tr key={`${idx}-${slotIdx}`}>
                {slotIdx === 0 && (
                  <td rowSpan={dayPlan.time_slots.length} className="day-cell">
                    {dayPlan.day}
                  </td>
                )}
                <td>{slot.time}</td>
                <td>{slot.subject}</td>
                <td>{slot.hours}h</td>
              </tr>
            ))
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudyPlanTable;

