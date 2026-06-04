```vue
<template>

  <div class="container mt-5">

    <h2>Student Registration</h2>

    <div class="mb-3">

      <label>Full Name</label>

      <input
        type="text"
        v-model="full_name"
        class="form-control"
      >

    </div>

    <div class="mb-3">

      <label>Email</label>

      <input
        type="email"
        v-model="email"
        class="form-control"
      >

    </div>

    <div class="mb-3">

      <label>Password</label>

      <input
        type="password"
        v-model="password"
        class="form-control"
      >

    </div>

    <div class="mb-3">

      <label>Department</label>

      <input
        type="text"
        v-model="department"
        class="form-control"
      >

    </div>

    <div class="mb-3">

      <label>CGPA</label>

      <input
        type="number"
        step="0.1"
        v-model="cgpa"
        class="form-control"
      >

    </div>

    <div class="mb-3">

      <label>Graduation Year</label>

      <input
        type="number"
        v-model="graduation_year"
        class="form-control"
      >

    </div>

    <div class="mb-3">

      <label>Skills</label>

      <input
        type="text"
        v-model="skills"
        class="form-control"
      >

    </div>

    <div class="mb-3">

      <label>Education</label>

      <textarea
        v-model="education"
        class="form-control"
      ></textarea>

    </div>

    <div class="mb-3">

      <label>Experience</label>

      <textarea
        v-model="experience"
        class="form-control"
      ></textarea>

    </div>

    <div class="mb-3">

      <label>Resume</label>

      <input
        type="file"
        class="form-control"
        @change="handleFileUpload"
      >

    </div>

    <button
      class="btn btn-primary"
      @click="registerStudent"
    >
      Register
    </button>

  </div>

</template>

<script>

export default {

  name: "RegisterStudent",

  data() {

    return {

      full_name: "",
      email: "",
      password: "",
      department: "",
      cgpa: "",
      graduation_year: "",
      skills: "",
      education: "",
      experience: "",
      resume: null

    }

  },

  methods: {

    handleFileUpload(event) {

      this.resume = event.target.files[0]

    },

    async registerStudent() {

      const formData = new FormData()

      formData.append(
        "full_name",
        this.full_name
      )

      formData.append(
        "email",
        this.email
      )

      formData.append(
        "password",
        this.password
      )

      formData.append(
        "department",
        this.department
      )

      formData.append(
        "cgpa",
        this.cgpa
      )

      formData.append(
        "graduation_year",
        this.graduation_year
      )

      formData.append(
        "skills",
        this.skills
      )

      formData.append(
        "education",
        this.education
      )

      formData.append(
        "experience",
        this.experience
      )

      if (this.resume) {

        formData.append(
          "resume",
          this.resume
        )

      }

      const response = await fetch(
        "http://127.0.0.1:5000/register/student",
        {

          method: "POST",

          body: formData

        }
      )

      const data = await response.json()

      alert(data.message)

      this.$router.push("/")

    }

  }

}

</script>

<style scoped>

</style>
```
