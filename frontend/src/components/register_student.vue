<template>

  <div class="container mt-5">

    <h2>Student Registration</h2>

    <div class="mb-3">
      <label>Full Name</label>
      <input type="text" v-model="full_name" class="form-control">
    </div>

    <div class="mb-3">
      <label>Email</label>
      <input type="email" v-model="email" class="form-control">
    </div>

    <div class="mb-3">
      <label>Password</label>
      <input type="password" v-model="password" class="form-control">
    </div>

    <div class="mb-3">
      <label>Department</label>
      <input type="text" v-model="department" class="form-control">
    </div>

    <div class="mb-3">
      <label>CGPA</label>
      <input type="number" v-model="cgpa" class="form-control">
    </div>

    <div class="mb-3">
      <label>Graduation Year</label>
      <input type="number" v-model="graduation_year" class="form-control">
    </div>

    <div class="mb-3">
      <label>Skills</label>
      <input type="text" v-model="skills" class="form-control">
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
      skills: ""

    }

  },

  methods: {

    async registerStudent() {

      const response = await fetch(
        "http://127.0.0.1:5000/register/student",
        {

          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({

            full_name: this.full_name,
            email: this.email,
            password: this.password,
            department: this.department,
            cgpa: this.cgpa,
            graduation_year: this.graduation_year,
            skills: this.skills

          })

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