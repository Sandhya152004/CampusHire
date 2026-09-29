<script setup>

import StudentNavbar from '../../components/StudentNavbar.vue'

import { ref, onMounted } from 'vue'

import api from '../../api'

const token = localStorage.getItem('token')

const profile = ref({})

const showEditModal = ref(false)

const successMessage = ref('')
const errorMessage = ref('')

const fetchProfile = async () => {

    try {

        const response = await api.get(

            '/student/profile',

            {

                headers: {

                    Authorization: `Bearer ${token}`

                }

            }

        )

        profile.value = response.data

    }

    catch (error) {

        console.log(error)

    }

}

const updateProfile = async () => {

    try {

        await api.put(
            '/student/profile',
            profile.value,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        await fetchProfile()

        successMessage.value = "Profile updated successfully."
        errorMessage.value = ""

        showEditModal.value = false

    } catch (error) {

        console.log(error)

        successMessage.value = ""
        errorMessage.value = "Unable to update profile."

    }

}

const resume = ref(null)

const handleResumeChange = (event) => {

    resume.value = event.target.files[0]

}

const uploadResume = async () => {

    console.log("Upload button clicked")

    if (!resume.value) {

        alert("No file selected")

        return

    }

    try {

        const formData = new FormData()

        formData.append(
            "resume",
            resume.value
        )

        console.log(formData)
        console.log(resume.value)

        const response = await api.post(

            "/student/resume",

            formData,

            {

                headers: {

                    Authorization: `Bearer ${token}`

                }

            }

        )

        console.log(response.data)

        alert("Resume Uploaded Successfully")

        fetchProfile()

    }

    catch (error) {

        console.log(error)

        console.log(error.response)

        alert(error.response?.data?.message || "Upload Failed")

    }
}

onMounted(() => {

    fetchProfile()

})

</script>

<template>

    <StudentNavbar />

    <div class="container mt-4">



        <div class="d-flex justify-content-between align-items-center mb-4">

            <div>

                <h2>My Profile</h2>

                <p class="text-muted">
                    View and manage your personal and academic information.
                </p>

            </div>

            <button class="btn btn-primary" @click="showEditModal = true">
                Edit Profile
            </button>

        </div>



        <div v-if="successMessage" class="alert alert-success">
            {{ successMessage }}
        </div>

        <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
        </div>



        <div class="card shadow-sm mb-4">

            <div class="card-header">

                <h5 class="mb-0">

                    Personal Information

                </h5>

            </div>

            <div class="card-body">

                <div class="row">

                    <div class="col-md-6">

                        <strong>Full Name</strong>

                        <p>{{ profile.full_name }}</p>

                    </div>

                    <div class="col-md-6">

                        <strong>Phone Number</strong>

                        <p>{{ profile.phone_number || "Not Available" }}</p>

                    </div>

                </div>

            </div>

        </div>



        <div class="card shadow-sm mb-4">

            <div class="card-header">

                <h5 class="mb-0">

                    Academic Information

                </h5>

            </div>

            <div class="card-body">

                <div class="row">

                    <div class="col-md-3">

                        <strong>Degree</strong>

                        <p>{{ profile.degree }}</p>

                    </div>

                    <div class="col-md-3">

                        <strong>Branch/Specialization</strong>

                        <p>{{ profile.branch }}</p>

                    </div>

                    <div class="col-md-3">

                        <strong>CGPA</strong>

                        <p>{{ profile.cgpa }}</p>

                    </div>

                    <div class="col-md-3">

                        <strong>Graduation Year</strong>

                        <p>{{ profile.graduation_year }}</p>

                    </div>

                </div>

            </div>

        </div>



        <div class="card shadow-sm mb-4">

            <div class="card-header">

                <h5 class="mb-0">

                    Skills

                </h5>

            </div>

            <div class="card-body">

                <p>

                    {{ profile.skills || "No skills added yet." }}

                </p>

            </div>

        </div>

      <

            <div class="card shadow-sm mb-4">

                <div class="card-header">

                    <h5 class="mb-0">

                        Resume

                    </h5>

                </div>

                <div class="card-body">

                    <div v-if="profile.resume_path">

                        <p class="text-success">

                            Resume uploaded successfully.

                        </p>

                        <a :href="`/uploads/resumes/${profile.resume_path}`" target="_blank"
                            class="btn btn-outline-primary mb-3">
                            View Resume
                        </a>

                    </div>

                    <div v-else>

                        <p class="text-muted">

                            No resume uploaded.

                        </p>

                    </div>

                    <input type="file" class="form-control mb-3" accept=".pdf" @change="handleResumeChange" />

                    <button class="btn btn-primary" @click="uploadResume">
                        Upload Resume
                    </button>

                </div>

            </div>



            <div v-if="showEditModal" class="modal d-block" style="background:rgba(0,0,0,.5)">

                <div class="modal-dialog modal-lg">

                    <div class="modal-content">

                        <div class="modal-header">

                            <h4>Edit Profile</h4>

                            <button class="btn-close" @click="showEditModal = false"></button>

                        </div>

                        <div class="modal-body">

                            <div class="row">

                                <div class="col-md-6 mb-3">

                                    <label class="form-label">

                                        Full Name

                                    </label>

                                    <input class="form-control" v-model="profile.full_name">

                                </div>

                                <div class="col-md-6 mb-3">

                                    <label class="form-label">

                                        Phone Number

                                    </label>

                                    <input class="form-control" v-model="profile.phone_number">

                                </div>

                                <div class="col-md-6 mb-3">

                          <label>Degree</label>

                          <select class="form-select" v-model="profile.degree">
                                <option value="">Select Degree</option>
                                <option value="B.Sc">B.Sc</option>
                                <option value="B.Tech">B.Tech</option>
                                <option value="BCA">BCA</option>
                                <option value="BBA">BBA</option>
                                <option value="B.Com">B.Com</option>
                                <option value="M.Sc">M.Sc</option>
                                <option value="M.Tech">M.Tech</option>
                                <option value="MCA">MCA</option>
                                <option value="MBA">MBA</option>
                            </select>

                                </div>

                                <div class="col-md-6 mb-3">

                                    <label class="form-label">

                              Branch/Specialization

                                    </label>

                                    <input class="form-control" v-model="profile.branch">

                                </div>

                                <div class="col-md-6 mb-3">

                                    <label class="form-label">

                                        CGPA

                                    </label>

                                    <input type="number" step="0.01" class="form-control" v-model="profile.cgpa">

                                </div>

                                <div class="col-md-6 mb-3">

                                    <label class="form-label">

                                        Graduation Year

                                    </label>

                                    <input type="number" class="form-control" v-model="profile.graduation_year">

                                </div>

                            </div>

                            <label class="form-label">

                                Skills

                            </label>

                            <textarea class="form-control" rows="4" v-model="profile.skills"></textarea>

                        </div>

                        <div class="modal-footer">

                            <button class="btn btn-secondary" @click="showEditModal = false">
                                Cancel
                            </button>

                            <button class="btn btn-primary" @click="updateProfile">
                                Save Changes
                            </button>

                        </div>

                    </div>

                </div>

            </div>

    </div>

</template>