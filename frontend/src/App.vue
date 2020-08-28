<template>
  <div id="app">
    <select v-model="country">
      <option v-for="country2 in possibleCountries.value" :key="country2">{{ country2 }}</option>
    </select>
    <select v-model="startDate">
      <option v-for="startDate2 in possibleStartDates.value" :key="startDate2">{{ startDate2.format('MM-DD-YYYY') }}</option>
    </select>
    <canvas id="chart"></canvas>
  </div>
</template>

<script lang="ts">
import { reactive, ref, watchEffect } from 'vue'
import moment, { Moment } from 'moment'
import { Chart } from 'chart.js'

const API_URL = 'http://localhost:8000'
const WINDOW_LEN = 36
const WINDOW_OFFSET = 7
const VALIDATION_SPLIT = 7

interface COVID19JSONRow {
  country: string;
  date: string;
  deaths: number;
  recoveries: number;
  cases: number;
}

interface COVID19Row {
  country: string;
  date: Moment;
  deaths: number;
  recoveries: number;
  cases: number;
}

interface COVID19Prediction {
  country: string;
  startDate: Moment;
  y: number;
}

let chart: Chart | null = null

export default {
  setup () {
    const data = reactive({ value: [] as COVID19Row[] })

    const country = ref('')
    const startDate = ref('')

    const possibleStartDates = reactive({ value: [] as Moment[] })
    const possibleCountries = reactive({ value: [] as string[] })

    watchEffect(() => {
      if ((country.value === '') || (startDate.value === '')) {
        return
      }

      const countryData = data.value.filter(v => (v.country === country.value))
      const tmpDates = countryData.map(v => v.date)
      const tmpDates2 = tmpDates.map(v => v.format('MM-DD-YYYY'))
      const futureDates = Array(VALIDATION_SPLIT)
        .fill(0)
        .map((_, idx) =>
          tmpDates[tmpDates.length - 1]
            .clone()
            .add(idx, 'day')
            .format('MM-DD-YYYY')
        )
      const dates = tmpDates2.concat(futureDates)

      const deaths = countryData.map(v => v.deaths)
      const recoveries = countryData.map(v => v.recoveries)
      const cases = countryData.map(v => v.cases)

      const xPrediction = moment(startDate.value, 'MM-DD-YYYY')
        .add(WINDOW_LEN + WINDOW_OFFSET - 1, 'day')
        .format('MM-DD-YYYY')

      fetch(`${API_URL}/predict/${country.value}/${startDate.value}`)
        .then(response => response.json())
        .then(jsonBody => jsonBody.data)
        .then(yPrediction => {
          chart && chart.destroy()

          chart = new Chart('chart', {
            type: 'line',
            data: {
              labels: dates,
              datasets: [
                { type: 'line', label: 'deaths', data: deaths },
                { type: 'line', label: 'recoveries', data: recoveries },
                { type: 'line', label: 'cases', data: cases },
                { type: 'scatter', label: 'deaths prediction', data: [{ x: xPrediction, y: yPrediction }] }
              ]
            }
          })
        })
    })

    fetch(`${API_URL}/data`)
      .then(response => response.json())
      .then(jsonBody => jsonBody.data)
      .then(jsonData => {
        data.value = jsonData
          .map((v: COVID19JSONRow) => {
            return {
              country: v.country,
              date: moment(v.date, 'MM/DD/YY'),
              deaths: v.deaths,
              recoveries: v.recoveries,
              cases: v.cases
            }
          })

        data.value.sort(v => -v.date.valueOf())

        const dates = [...new Set(data.value.map(v => v.date))]
        dates.sort(v => -v.valueOf())

        possibleStartDates.value = dates.slice(0, VALIDATION_SPLIT)
        possibleCountries.value = [...new Set(data.value.map(v => v.country))]
      })

    return {
      country: country,
      startDate: startDate,

      possibleStartDates: possibleStartDates,
      possibleCountries: possibleCountries
    }
  }
}
</script>
