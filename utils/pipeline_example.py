from .utils import (
    handle_add_dataset,
    handle_add_model,
    handle_add_operation,
    handle_add_preprocessing,
    handle_add_service,
    update_elements_from_popovers,
    create_dataset_popover_body,
    create_preprocessing_popover_body,
    create_model_popover_body,
    create_operation_popover_body,
    create_service_popover_body
)


def create_pipeline_example(redis_instance, session_id):
    flow_direction = 'vertical'
    elements = []
    popovers = []

    dataset_popover_body = create_dataset_popover_body(
        dataset_name='Iris',
        redis_instance=redis_instance,
        session_id=session_id,
        index='node-element-dataset-example'
    )
    elements, popovers = handle_add_dataset(
        elements=elements,
        popovers=popovers,
        id_index="example",
        position={"x": 20, "y": 0},
        flow_direction=flow_direction,
        popover_body=dataset_popover_body,
    )
    preprocessing_popover_body = create_preprocessing_popover_body(
        preprocessing_name='Train/Test split',
        index='node-element-preprocessing-example'
    )
    elements, popovers = handle_add_preprocessing(
        elements=elements,
        popovers=popovers,
        id_index="example",
        position={"x": 30, "y": 100},
        flow_direction=flow_direction,
        popover_body=preprocessing_popover_body
    )
    flow_direction = "horizontal"
    model1_popover_body = create_model_popover_body(
        model_name='Logistic Classifier'
    )
    elements, popovers = handle_add_model(
        elements=elements,
        popovers=popovers,
        id_index="example",
        position={"x": 330, "y": 150},
        flow_direction=flow_direction,
        popover_body=model1_popover_body
    )
    model2_popover_body = create_model_popover_body(
        model_name='Logistic Classifier'
    )
    elements, popovers = handle_add_model(
        elements=elements,
        popovers=popovers,
        id_index="example2",
        position={"x": 300, "y": 250},
        flow_direction=flow_direction,
        popover_body=model2_popover_body
    )
    operation_popover_body = create_operation_popover_body(
        operation_name='Compare & Select',
        index='node-element-operation-example'
    )
    elements, popovers = handle_add_operation(
        elements=elements,
        popovers=popovers,
        id_index="example",
        position={"x": 600, "y": 200},
        flow_direction=flow_direction,
        popover_body=operation_popover_body
    )
    service1_popover_body = create_service_popover_body(
        service_name='Deploy',
        index='node-element-service-example',
        value=[1]
    )
    elements, popovers = handle_add_service(
        elements=elements,
        popovers=popovers,
        id_index="example",
        position={"x": 900, "y": 250},
        flow_direction=flow_direction,
        popover_body=service1_popover_body
    )
    service2_popover_body = create_service_popover_body(
        service_name='Report',
        index='node-element-service-example2',
        value='example@plot.ly'
    )
    elements, popovers = handle_add_service(
        elements=elements,
        popovers=popovers,
        id_index="example2",
        position={"x": 900, "y": 150},
        flow_direction=flow_direction,
        popover_body=service2_popover_body
    )

    elements = update_elements_from_popovers(
        type="dataset",
        index="node-element-dataset-example",
        label="Iris",
        elements=elements
    )
    elements = update_elements_from_popovers(
        type="preprocessing",
        index="node-element-preprocessing-example",
        label="Train/Test split",
        elements=elements,
    )
    elements = update_elements_from_popovers(
        type="model",
        index="node-element-model-example",
        label="Logistic Classifier",
        elements=elements
    )
    elements = update_elements_from_popovers(
        type="model",
        index="node-element-model-example",
        label="XGBoost",
        elements=elements
    )
    elements = update_elements_from_popovers(
        type="model", 
        index="node-element-model-example2",
        label="Logistic Classifier",
        elements=elements
    )
    elements = update_elements_from_popovers(
        type="operation",
        index="node-element-operation-example",
        label="Compare & Select",
        elements=elements
    )
    elements = update_elements_from_popovers(
        type="service",
        index="node-element-service-example",
        label="Deploy",
        elements=elements
    )
    elements = update_elements_from_popovers(
        type="service",
        index="node-element-service-example2",
        label="Report",
        elements=elements
    )

    connections_elements = [
        {
            "source": "node-element-dataset-example",
            "target": "node-element-preprocessing-example",
            "id": "edge-dataset-preprocessing-example",
        },
        {
            "source": "node-element-preprocessing-example",
            "target": "node-element-model-example",
            "id": "edge-preprocessing-model-example",
        },
        {
            "source": "node-element-preprocessing-example",
            "target": "node-element-model-example2",
            "id": "edge-preprocessing-model-example2",
        },
        {
            "source": "node-element-model-example",
            "target": "node-element-operation-example",
            "id": "edge-model-operation-example",
        },
        {
            "source": "node-element-model-example2",
            "target": "node-element-operation-example",
            "id": "edge-model-operation-example2",
        },
        {
            "source": "node-element-operation-example",
            "target": "node-element-service-example",
            "id": "edge-operation-service-example",
        },
        {
            "source": "node-element-operation-example",
            "target": "node-element-service-example2",
            "id": "edge-operation-service-example2",
        },
    ]

    elements = elements + connections_elements

    return elements, popovers
