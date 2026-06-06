
<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between mb-4">

      <h2>Job Applications</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/company-jobs')"
      >
        Back
      </button>

    </div>

    <div
      v-for="application in applications"
      :key="application.application_id"
      class="card p-3 mb-3"
    >

      <h5>
        {{ application.student_name }}
      </h5>

      <p>
        Department:
        {{ application.department }}
      </p>

      <p>
        CGPA:
        {{ application.cgpa }}
      </p>

      <p>
        Resume:
        <a
          :href="application.resume"
          target="_blank"
          v-if="application.resume"
        >
          View Resume
        </a>

        <span v-else>
          No Resume Uploaded
        </span>
      </p>

      <p>
        Status:
        {{ application.status }}
      </p>

      <p>
        Interview Date:
        {{
          application.interview_date
            ? new Date(application.interview_date).toLocaleString()
            : "Not Scheduled"
        }}
      </p>


      <div class="mt-3">

        <label>Feedback</label>

        <textarea
          v-model="application.feedback"
          class="form-control"
          placeholder="Enter feedback"
        ></textarea>

      </div>


      <div
        v-if="application.status === 'applied'"
        class="mt-3"
      >

        <input
          type="datetime-local"
          v-model="application.scheduled_date"
          class="form-control mb-2"
        >

        <button
          class="btn btn-warning"
          @click="scheduleInterview(application)"
        >
          Schedule Interview
        </button>

      </div>


      <div
        v-if="
          application.status === 'interview scheduled' ||
          application.status === 'placed' ||
          application.status === 'rejected'
        "
        class="d-flex gap-2 flex-wrap mt-3"
      >

        <button
          class="btn btn-danger"
          @click="updateStatus(application, 'rejected')"
        >
          Reject
        </button>

        <button
          class="btn btn-success"
          @click="updateStatus(application, 'placed')"
        >
          Place
        </button>

      </div>

    </div>

  </div>

</template>

<script>

export default {

  name: "JobApplications",

  data() {

    return {

      applications: []

    }

  },

  methods: {

    async loadApplications() {

      const token = localStorage.getItem("token")

      const jobId = this.$route.params.jobId

      const response = await fetch(
        `http://127.0.0.1:5000/company/job-applications/${jobId}`,
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.applications = data

    },

    async updateStatus(application, status) {

      const token = localStorage.getItem("token")

      const response = await fetch(
        `http://127.0.0.1:5000/company/update-application/${application.application_id}`,
        {

          method: "PUT",

          headers: {

            "Content-Type": "application/json",

            "Authorization": "Bearer " + token

          },

          body: JSON.stringify({

            status: status,

            feedback: application.feedback

          })

        }
      )

      const data = await response.json()

      alert(data.message)

      this.loadApplications()

    },

    async scheduleInterview(application) {

      const token = localStorage.getItem("token")

      const response = await fetch(
        `http://127.0.0.1:5000/company/schedule-interview/${application.application_id}`,
        {

          method: "PUT",

          headers: {

            "Content-Type": "application/json",

            "Authorization": "Bearer " + token

          },

          body: JSON.stringify({

            interview_date: application.scheduled_date

          })

        }
      )

      const data = await response.json()

      alert(data.message)

      this.loadApplications()

    }

  },

  mounted() {

    this.loadApplications()

  }

}

</script>

<style scoped>

.card {
  border-radius: 12px;
}

textarea {
  resize: none;
}

</style>
```
