<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h2>Edit Profile</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/student')"
      >
        Back
      </button>

    </div>

    <div class="card p-4">

      <div class="mb-3">

        <label>Full Name</label>

        <input
          type="text"
          class="form-control"
          v-model="student.full_name"
        >

      </div>

      <div class="mb-3">

        <label>Department</label>

        <input
          type="text"
          class="form-control"
          v-model="student.department"
        >

      </div>

      <div class="mb-3">

        <label>CGPA</label>

        <input
          type="number"
          step="0.1"
          class="form-control"
          v-model="student.cgpa"
        >

      </div>

      <div class="mb-3">

        <label>Graduation Year</label>

        <input
          type="number"
          class="form-control"
          v-model="student.graduation_year"
        >

      </div>

      <div class="mb-3">

        <label>Skills</label>

        <input
          type="text"
          class="form-control"
          v-model="student.skills"
        >

      </div>

      <div class="mb-3">

        <label>Education</label>

        <textarea
          class="form-control"
          v-model="student.education"
        ></textarea>

      </div>

      <div class="mb-3">

        <label>Experience</label>

        <textarea
          class="form-control"
          v-model="student.experience"
        ></textarea>

      </div>

      <div class="mb-3">

        <label>Upload Resume</label>

        <p
          v-if="student.resume"
          class="mb-2"
        >

          Current Resume:
          
          <a
            :href="`http://127.0.0.1:5000/uploads/${student.resume}`"
            target="_blank"
          >
            {{ student.resume }}
          </a>

        </p>

        <input
          type="file"
          class="form-control"
          @change="handleFileUpload"
        >

      </div>

      <button
        class="btn btn-primary"
        @click="updateProfile"
      >
        Update Profile
      </button>

    </div>

  </div>

</template>

<script>

export default {

  name: "EditProfile",

  data() {

    return {

      student: {},

      resumeFile: null

    }

  },

  methods: {

    async loadProfile() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/student/dashboard",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.student = data

    },

    handleFileUpload(event) {

      this.resumeFile = event.target.files[0]

    },

    async updateProfile() {

      const token = localStorage.getItem("token")

      // UPDATE PROFILE

      const response = await fetch(
        "http://127.0.0.1:5000/student/update-profile",
        {

          method: "PUT",

          headers: {

            "Content-Type": "application/json",

            "Authorization": "Bearer " + token

          },

          body: JSON.stringify(this.student)

        }
      )

      const data = await response.json()

      // UPLOAD RESUME

      if (this.resumeFile) {

        const formData = new FormData()

        formData.append(
          "resume",
          this.resumeFile
        )

        await fetch(
          "http://127.0.0.1:5000/student/upload-resume",
          {

            method: "POST",

            headers: {
              "Authorization": "Bearer " + token
            },

            body: formData

          }
        )

      }

      alert(data.message)

      this.$router.push("/student")

    }

  },

  mounted() {

    this.loadProfile()

  }

}

</script>

<style scoped>

.card {
  border-radius: 12px;
}

</style>