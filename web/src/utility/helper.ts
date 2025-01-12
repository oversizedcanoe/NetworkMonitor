export function dateToLocal(date: Date | string, includeDate: boolean = false): string {
    let local = '';
    let tempDate: Date;

    if(date instanceof Date) {
        tempDate = date;
    }
    else {
        tempDate = new Date(date + 'Z');
    }

    if (includeDate) {
        //Sun Jan 12 2025 14:32:05 GMT-0500 (Eastern Standard Time)
        local = tempDate.toString()
    } else {
        //14:32:05 GMT-0500 (Eastern Standard Time)
        local = tempDate.toTimeString()
    }

    return local.substring(0, local.indexOf('('));
}