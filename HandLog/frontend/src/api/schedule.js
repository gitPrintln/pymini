import axios from 'axios';

async function saveSchedule(schedule) {
  const response = await axios.post("http://localhost:5000/api/schedules/", {
    date: schedule.date,
    title: schedule.title,
    memo: schedule.memo
  });
  console.log(response.data);
}