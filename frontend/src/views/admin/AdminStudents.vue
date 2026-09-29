<script setup>

import AdminNavbar from '../../components/AdminNavbar.vue'

import { ref, onMounted, computed } from 'vue'

import api from '../../api'

const token = localStorage.getItem('token')

const students = ref([])
const search = ref('')

const fetchStudents = async () => {

    const response = await api.get(

        '/admin/students',

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    students.value = response.data

}

const blacklistStudent = async(student)=>{

    const reason = prompt(

        "Enter blacklist reason"

    )

    if(!reason) return

    await api.put(

        `/admin/student/${student.id}/blacklist`,

        {

            reason:reason

        },

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    fetchStudents()

}

const restoreStudent = async(student)=>{

    await api.put(

        `/admin/student/${student.id}/restore`,

        {},

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    fetchStudents()

}

const filteredStudents = computed(()=>{

return students.value.filter(student=>

    student.full_name
    .toLowerCase()
    .includes(search.value.toLowerCase())

)

})

onMounted(()=>{

    fetchStudents()

})

</script>


<template>

    <AdminNavbar />
    
    <div class="container mt-4">
    
        <div class="d-flex justify-content-between align-items-center mb-4">
    
            <div>
    
                <h2>Student Management</h2>
    
                <p class="text-muted">
    
                    Manage all registered students.
    
                </p>
    
            </div>
    
        </div>
        <input

            class="form-control mb-4"

            placeholder="Search student..."

            v-model="search"

            >

    
        <h4 class="mb-3">
    
            Active Students
    
        </h4>
    
        <div
    
            v-for="student in filteredStudents.filter(s => !s.is_blacklisted)"
    
            :key="student.id"
    
            class="card shadow-sm mb-3"
    
        >
    
            <div class="card-body">
    
                <div class="row">
    
                    <div class="col-md-8">
    
                        <h5>
    
                            {{ student.full_name }}
    
                        </h5>
    
                        <p class="mb-1">
    
                            <strong>Degree:</strong>
    
                            {{ student.degree }}
    
                        </p>
    
                        <p class="mb-1">
    
                            <strong>Branch/Specialization:</strong>
    
                            {{ student.branch }}
    
                        </p>
    
                        <p class="mb-1">
    
                            <strong>CGPA:</strong>
    
                            {{ student.cgpa }}
    
                        </p>
    
                        <p class="mb-1">
    
                            <strong>Graduation Year:</strong>
    
                            {{ student.graduation_year }}
    
                        </p>
    
                        <p class="mb-1">
    
                            <strong>Phone:</strong>
    
                            {{ student.phone_number }}
    
                        </p>
    
                        <p>
    
                            <strong>Skills:</strong>
    
                            {{ student.skills }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4 text-end">
    
                        <a
    
                            v-if="student.resume_path"
    
                            :href="`/uploads/resumes/${student.resume_path}`"
    
                            target="_blank"
    
                            class="btn btn-outline-primary mb-2 w-100"
    
                        >
    
                            View Resume
    
                        </a>
    
                        <button
    
                            class="btn btn-danger w-100"
    
                            @click="blacklistStudent(student)"
    
                        >
    
                            Blacklist Student
    
                        </button>
    
                    </div>
    
                </div>
    
            </div>
    
        </div>
    
        <hr class="my-5">
    

    
        <h4 class="mb-3">
    
            Blacklisted Students
    
        </h4>
    
        <div
    
            v-for="student in students.filter(s => s.is_blacklisted)"
    
            :key="student.id"
    
            class="card border-danger shadow-sm mb-3"
    
        >
    
            <div class="card-body">
    
                <div class="row">
    
                    <div class="col-md-8">
    
                        <h5>
    
                            {{ student.full_name }}
    
                        </h5>
    
                        <p>
    
                            <strong>Reason:</strong>
    
                            {{ student.blacklist_reason }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4 text-end">
    
                        <button
    
                            class="btn btn-success"
    
                            @click="restoreStudent(student)"
    
                        >
    
                            Restore Student
    
                        </button>
    
                    </div>
    
                </div>
    
            </div>
    
        </div>
    
    </div>
    
    </template>