export class ModalService {
    private static openFunction: (isOpen: boolean, modalData: any) => void;

    public static setOpenFunction(f: (isOpen: boolean, modalData: any) => void) {
        ModalService.openFunction = f;
    }
    
    public static setOpen(isOpen: boolean, modalData: any) {
        if (ModalService.openFunction) {
            ModalService.openFunction(isOpen, modalData);
        } else {
            console.error("ModalHelper called before setOpenFunction")
        }
    }
}
