<template>
  <div>
    <h2>{{ year }}년 {{ month }}월</h2>
    <button @click="prevMonth">이전</button>
    <button @click="nextMonth">다음</button>

    <table border="1" cellspacing="0" cellpadding="5">
      <thead>
        <tr>
          <th v-for="day in weekDays" :key="day">{{ day }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(week, wIndex) in calendar" :key="wIndex">
          <td v-for="(date, dIndex) in week" :key="dIndex"
              :class="{ today: isToday(date) }"
              @click="date && onDateClick(date)">
            {{ date || '' }}
          </td>
        </tr>
      </tbody>
    </table>

    <MyModal
      v-if="isModalOpen"
      :date="selectedDate"
      :memo="scheduleMemo"
      @close="isModalOpen = false"
    />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import axios from 'axios';

const weekDays = ['일', '월', '화', '수', '목', '금', '토']

const today = new Date();
const year = ref(today.getFullYear());
const month = ref(today.getMonth() + 1);

const calendar = computed(() => {
  const firstDay = getFirstDayOfWeek(year.value, month.value);
  const daysCount = getDaysInMonth(year.value, month.value);

  // 전체 필요한 일수(전 달의 날짜는 빈부분으로 포함 + 이번 달의 총 일수)
  const total = Math.ceil((firstDay + daysCount) / 7) * 7

  // 각각의 날짜 계산해서 1~total 사이면 달력 날짜 기입, else null -> null이면 위쪽에서 ''로 변환해줌
  const dates = []
  for(let i = 0;i < total;i++) {
    const dayNum = i - firstDay + 1
    if(dayNum > 0 && dayNum <= daysCount) {
      dates.push(dayNum)
    } else {
      dates.push(null)
    }
  }

  // 7개씩 끊어서 한 주씩 나눔
  const weeks = []
  for(let i = 0;i < dates.length;i += 7){
    weeks.push(dates.slice(i, i + 7))
  }
  return weeks
})

// 한 달의 총 일수 가져오기
const getDaysInMonth = (year, month) => {
  return new Date(year, month, 0).getDate();
}

// 이번 달의 첫 날이 무슨 요일인지
const getFirstDayOfWeek = (year, month) => {
  return new Date(year, month -1, 1).getDay();
}

const isToday = (date) => {
  if(!date) return false
  return (
    date === today.getDate() &&
    month.value === today.getMonth() + 1 &&
    year.value === today.getFullYear()
  )
}

const onDateClick = (date) => { // 현재 클릭한 곳의 날짜 콘솔 출력
  console.log(`${year.value}년 ${month.value}월 ${date}일!!`)
}

const prevMonth = () => {
  if(month.value === 1){ // 1월이면 연도 - 1, 달 = 12월
    year.value -= 1
    month.value = 12
  } else {
    month.value -= 1
  }
}

const nextMonth = () => {
  if(month.value === 12){ // 12월이면 연도 + 1, 달 = 1월
    year.value += 1
    month.value = 1
  } else {
    month.value += 1
  }
}

// 스케쥴 등록 api
const schedules = ref([])

onMounted(async () => {
  const response = await axios.get('http://localhost:5000/api/schedules/')
  schedules.value = response.data
})

const isModalOpen = ref(false)

</script>

<style scoped>
table {
  width: 100%;
  text-align: center;
}
td {
  cursor: pointer;
  height: 50px;
  vertical-align: middle;
}
.today {
  background-color: #3b82f6;
  color: white;
  font-weight: bold;
}
</style>