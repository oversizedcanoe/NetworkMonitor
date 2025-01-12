import axios from "axios";

export class BackendService {
    readonly apiUrl: string;

    constructor() {
        this.apiUrl = 'http://192.168.2.34:8080/';
    }

    async get<T>(endpoint: string): Promise<T | undefined> {
        try {
            const response = await axios.get(this.apiUrl  + endpoint);

            if (response.status == 200) {
                return response.data as T;
            } else {
                this.handleError('Failed to convert response')
            }
        }
        catch (error) {
            this.handleError(error);
        }
    }

    async post(endpoint: string, data: object): Promise<string> {
        try {
            await axios.post(this.apiUrl + endpoint, data);
            return ''
        }
        catch (error: any) {
            this.handleError(error);
            return 'Error'
        }
    }

    handleError(error: any) {
        if(error instanceof String){
            alert(error);
        }

        alert('Error occurred, check console');
        console.error(error);
    }

}
