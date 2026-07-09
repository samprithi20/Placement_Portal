<template>

<div class="container mt-5">
  <div class="d-flex justify-content-between mb-4">
  <h2>Generated Report</h2>
  <button class="btn btn-secondary"
  @click="$router.push('/admin')">Back</button>
    </div>
  <div
    v-if="report.filename"
    class="card p-3"
  >
    <h5>{{ report.filename }}</h5>

    <a
      :href="report.url"
      target="_blank"
      class="btn btn-primary">
      Open Report
    </a>

  </div>

  <div
    v-else
    class="alert alert-warning"
  >
    No report available
  </div>

</div>

</template>



<script>

export default {
  name : "Report",

  data() {

    return {

      report: {}

    }

  },

  async mounted() {

    const token = localStorage.getItem("token")

    const res = await fetch(
      "http://127.0.0.1:5000/admin/reports",
      {
        headers: {
          Authorization: "Bearer " + token
        }
      }
    )

    this.report = await res.json()

  }

}

</script>