<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between mb-4">

      <h2>All Jobs</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/admin')"
      >
        Back
      </button>

    </div>

    <div
        v-for="job in jobs"
        :key="job.id"
        class="card p-4 mb-4 shadow-sm"
      >

        <h4>{{ job.title }}</h4>

        <p>
          <strong>Company:</strong>
          {{ job.company_name }}
        </p>

        <p>
          <strong>Description:</strong>
          {{ job.description }}
        </p>

        <p>
          <strong>Location:</strong>
          {{ job.location }}
        </p>

        <p>
          <strong>Salary:</strong>
          {{ job.salary }}
        </p>

        <p>
          <strong>Status:</strong>
          {{ job.status }}
        </p>

        <hr>

        <h5>Eligibility Criteria</h5>

        <p>
          <strong>Eligible Departments:</strong>
          {{ job.eligible_department }}
        </p>

        <p>
          <strong>Eligible Batch:</strong>
          {{ job.eligible_batch }}
        </p>

        <p>
          <strong>Minimum CGPA:</strong>
          {{ job.minimum_cgpa }}
        </p>

        <hr>

        <h5>Additional Information</h5>

        <p>
          <strong>Required Skills:</strong>
          {{ job.required_skills }}
        </p>

        <p>
          <strong>Experience Required:</strong>
          {{ job.experience_required }}
        </p>

        <p>
          <strong>Benefits:</strong>
          {{ job.benefits }}
        </p>

        <p>
          <strong>Application Deadline:</strong>
          {{ job.application_deadline }}
        </p>

        <p>
          <strong>Total Applications:</strong>
          {{ job.applications }}
        </p>

      </div>

  </div>

</template>

<script>

export default {

  name: "AllJobs",

  data() {

    return {

      jobs: []

    }

  },

  methods: {

    async loadJobs() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/admin/jobs",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.jobs = data

    }

  },

  mounted() {

    this.loadJobs()

  }

}

</script>