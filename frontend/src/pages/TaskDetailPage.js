import {useParams} from 'react-router-dom';

import TaskDetail from '../components/Profile/TaskDetail';

const TaskDetailPage = () => {
    const params = useParams();
    // console.log(params.taskName)
    return <TaskDetail params={params.taskName} />
}

export default TaskDetailPage;