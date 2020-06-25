<template>
  <div class="home">
    <AddCourseForm @courseadd="validate">
    </AddCourseForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import AddCourseForm from '@/components/AddCourse.vue';

export default {
  name: 'AddCourse',
  components: {
    AddCourseForm,
  },
  methods: {
    validate(newcourse) {
      if (newcourse.id === null || newcourse.id === '') {
        alert('Fill in user name');
      }
      if (newcourse.name === null || newcourse.name === '') {
        alert('Fill in first name');
      }
      this.add(newcourse);
    },
    add(data) {
      const path = 'http://localhost:5000/courses/add_course_json';
      axios.post(path, data)
        .then((res) => {
          alert(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
