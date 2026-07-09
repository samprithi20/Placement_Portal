<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h2>Create Placement Drive</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/company')"
      >
        Back
      </button>

    </div>

    <div class="card p-4">
      <div class="mb-3">

        <label>Job Title</label>

        <input
          type="text"
          v-model="title"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>Description</label>

        <textarea
          v-model="description"
          class="form-control"
        ></textarea>

      </div>

      <div class="mb-3">

        <label>Location</label>

        <input
          type="text"
          v-model="location"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>Salary</label>

        <input
          type="text"
          v-model="salary"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>Required Skills (Comma Separated)</label>

        <input
          type="text"
          v-model="required_skills"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>Experience Required</label>

        <input
          type="text"
          v-model="experience_required"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>Benefits</label>

        <input
          type="text"
          v-model="benefits"
          class="form-control"
        >
      </div>

      <hr>

      <h4 class="mb-3">
        Eligibility Criteria
      </h4>

      <div class="mb-3">
        <label>Eligible Department</label>

        <input type="text"
          v-model="eligible_department"
          class="form-control"
        >

      </div>

      <div class="mb-3">
        <label>Minimum CGPA</label>

        <input
          type="number"
          step="0.1"
          v-model="minimum_cgpa"
          class="form-control"
        >

      </div>

      <div class="mb-3">
        <label>Eligible Graduation Year</label>

        <input
          type="text"
          v-model="eligible_batch"
          class="form-control"
        >

      </div>

      <div class="mb-3">
        <label>Application Deadline</label>

        <input
          type="date"
          v-model="application_deadline"
          class="form-control"
        >

      </div>

      <button class="btn btn-primary"
        @click="postJob"
      > Create Placement Drive </button>
    </div>
  </div>

</template>

<script>

export default {

  name: "PostJob",

  data() {

    return {
      title: "",
      description: "",
      location: "",
      salary: "",
      required_skills: "",
      experience_required: "",
      benefits: "",
      eligible_department: "",
      minimum_cgpa: "",
      eligible_batch: "",
      application_deadline: ""
    }
  },

  methods: {

    async postJob() {
      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/company/create-job",
        {

          method: "POST",

          headers: {

            "Content-Type": "application/json",

            "Authorization": "Bearer " + token

          },

          body: JSON.stringify({
            title: this.title,
            description: this.description,
            location: this.location,
            salary: this.salary,
            required_skills: this.required_skills,
            experience_required: this.experience_required,
            benefits: this.benefits,
            eligible_department: this.eligible_department,
            minimum_cgpa: this.minimum_cgpa,
            eligible_batch: this.eligible_batch,
            application_deadline: this.application_deadline
          })
        }
      )

      const data = await response.json()

      alert(data.message)

      if (response.ok) {
        this.$router.push("/company")
      }

    }

  }

}

</script>

<style scoped>

.card {
  border-radius: 12px;
}

</style>